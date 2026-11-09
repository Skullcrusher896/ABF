"""Find where a key is defined (and optionally used) in ABA and base Ante Bellum, printing only the block.

Usage: python -I find.py KEY [KEY ...] [--in aba|ab|both] [--usages] [--max-lines N] [--ab PATH]

Matches:  KEY = { ... }   (missions, effects, triggers, modifiers, reforms, decisions, ...)
          id = KEY        (events: prints the whole event)
          KEY: "..."      (localisation)
Output is prefixed by [ABA] or [AB] so you can see which definition wins / is overridden.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from abpath import REPO, SCAN_DIRS, ab_path, need_ab  # noqa: E402


def code_only(line):
    out, q = [], False
    for c in line:
        if c == '"':
            q = not q
        elif c == "#" and not q:
            break
        out.append(c)
    return "".join(out)


def files(root):
    for d in SCAN_DIRS:
        base = root / d
        if base.exists():
            for p in base.rglob("*"):
                if p.suffix in (".txt", ".yml", ".gui", ".lua") and p.is_file():
                    yield p


def search(root, label, keys, usages, max_lines):
    pats = {k: (re.compile(rf"^\s*{re.escape(k)}\s*=\s*\{{"),
                re.compile(rf"^\s*id\s*=\s*{re.escape(k)}\s*$"),
                re.compile(rf"^\s*{re.escape(k)}:\d*\s*\""),
                re.compile(rf"(?<![\w.]){re.escape(k)}(?![\w.])")) for k in keys}
    found = {k: 0 for k in keys}
    used = {k: [] for k in keys}
    for p in files(root):
        try:
            text = p.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        hit = [k for k in keys if k in text]
        if not hit:
            continue
        lines = text.splitlines()
        depth, top_start = 0, 0
        depths = []
        for i, l in enumerate(lines):
            if depth == 0 and "{" in code_only(l):
                top_start = i
            depths.append((depth, top_start))
            c = code_only(l)
            depth = max(0, depth + c.count("{") - c.count("}"))
        rel = p.relative_to(root).as_posix()
        for k in hit:
            block_re, id_re, loc_re, word_re = pats[k]
            for i, l in enumerate(lines):
                start = None
                if loc_re.match(l):
                    print(f"[{label}] {rel}:{i+1}\n{l.strip()}\n")
                    found[k] += 1
                    continue
                if block_re.match(code_only(l)):
                    start = i
                elif id_re.match(code_only(l)):
                    start = depths[i][1]
                if start is not None:
                    found[k] += 1
                    d, end = 0, start
                    for j in range(start, len(lines)):
                        c = code_only(lines[j])
                        d += c.count("{") - c.count("}")
                        end = j
                        if d <= 0 and "{" in "".join(lines[start:j + 1]):
                            break
                    shown = lines[start:min(end + 1, start + max_lines)]
                    more = end + 1 - start - len(shown)
                    print(f"[{label}] {rel}:{start+1}-{end+1}")
                    print("\n".join(shown))
                    if more > 0:
                        print(f"... ({more} more lines; read {rel} offset {start+len(shown)+1})")
                    print()
                elif usages and word_re.search(code_only(l) if p.suffix != ".yml" else l):
                    used[k].append(f"{rel}:{i+1}")
    return found, used


def main():
    a = sys.argv[1:]
    def opt(name, default=None):
        if name in a:
            i = a.index(name)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return default
    where = opt("--in", "both")
    max_lines = int(opt("--max-lines", "80"))
    ab_arg = opt("--ab")
    usages = "--usages" in a
    keys = [x for x in a if not x.startswith("--")]
    if not keys:
        raise SystemExit(__doc__)
    roots = []
    if where in ("aba", "both"):
        roots.append((REPO, "ABA"))
    if where in ("ab", "both"):
        p = need_ab(ab_arg) if where == "ab" else ab_path(ab_arg)
        if p:
            roots.append((p, "AB"))
        else:
            print("NOTE: base AB not found; searched ABA only (set AB_PATH)\n")
    for root, label in roots:
        found, used = search(root, label, keys, usages, max_lines)
        for k in keys:
            if not found[k]:
                print(f"[{label}] no definition of '{k}'")
            if usages:
                u = used[k]
                print(f"[{label}] '{k}' used {len(u)}x" + (": " + ", ".join(u[:30]) if u else "")
                      + (" ..." if len(u) > 30 else ""))


if __name__ == "__main__":
    main()
