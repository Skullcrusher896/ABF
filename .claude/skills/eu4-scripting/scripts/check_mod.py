"""Static checks for the ABA EU4 submod.

Usage: python -I .claude/skills/eu4-scripting/scripts/check_mod.py
           [--ab <Ante Bellum folder>] [--verbose] [--stub] [--paths file_or_dir ...]
       Base AB is found via --ab, the AB_PATH env var, or a sibling ../ab folder.
       --stub prints missing loc keys as ready-to-paste ` key: "TODO"` lines. --paths must come last.

Checks:
  1. Brace balance in game script .txt files (ignoring comments and strings).
  2. Localisation .yml files start with a UTF-8 BOM and an l_<language>: header.
  3. Event title/desc/option keys and mission _title/_desc keys exist in localisation.
     (Keys may legitimately live in base Ante Bellum; those are reported as warnings.)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aba-lookup" / "scripts"))
from abpath import REPO, ab_path  # noqa: E402

SCRIPT_DIRS = ["common", "events", "missions", "decisions", "history", "customizable_localization", "interface"]


def strip_comments_and_strings(text):
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            if c == '"':
                in_str = False
            elif c == "\n":
                in_str = False
                out.append(c)
        elif c == '"':
            in_str = True
        elif c == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def read(p):
    return p.read_text(encoding="utf-8-sig", errors="replace")


def check_braces(path):
    text = strip_comments_and_strings(read(path))
    depth = 0
    line = 1
    for ch in text:
        if ch == "\n":
            line += 1
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return f"extra '}}' at line {line}"
    if depth > 0:
        return f"{depth} unclosed '{{' at end of file"
    return None


def load_loc(root):
    keys, problems = set(), []
    key_re = re.compile(r"^\s+([A-Za-z0-9_.\-]+):\d*\s*\"")
    for p in (root / "localisation").rglob("*.yml"):
        raw = p.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            problems.append(f"{p.relative_to(root)}: missing UTF-8 BOM")
        text = raw.decode("utf-8-sig", errors="replace")
        first = next((l for l in text.splitlines() if l.strip() and not l.strip().startswith("#")), "")
        if not re.match(r"^l_[a-z_]+:\s*$", first.strip()):
            problems.append(f"{p.relative_to(root)}: first line is not an l_<language>: header")
        for l in text.splitlines():
            m = key_re.match(l)
            if m:
                keys.add(m.group(1))
    return keys, problems


def referenced_keys(root, files):
    refs = []
    ev = re.compile(r"^\s*(title|desc|name)\s*=\s*\"?([A-Za-z0-9_.\-]+)\"?\s*$")
    for p in files:
        rel = p.relative_to(root).as_posix()
        if rel.startswith("events/"):
            for i, l in enumerate(read(p).splitlines(), 1):
                m = ev.match(l.split("#")[0])
                if m and "." in m.group(2):
                    refs.append((rel, i, m.group(2)))
        elif rel.startswith("missions/"):
            text = strip_comments_and_strings(read(p))
            depth = 0
            for i, l in enumerate(text.splitlines(), 1):
                m = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{", l)
                if m and depth == 1 and m.group(1) not in ("potential", "potential_on_load", "ai_weight", "trigger"):
                    refs.append((rel, i, m.group(1) + "_title"))
                    refs.append((rel, i, m.group(1) + "_desc"))
                depth += l.count("{") - l.count("}")
    return refs


def main():
    args = sys.argv[1:]
    root = REPO
    only = None
    if "--paths" in args:
        only = [(root / a).resolve() for a in args[args.index("--paths") + 1:]]

    files = []
    for d in SCRIPT_DIRS:
        files += list((root / d).rglob("*.txt")) if (root / d).exists() else []
    if only:
        files = [f for f in files if any(f == o or o in f.parents for o in only)]

    errors, warnings = [], []
    for f in files:
        msg = check_braces(f)
        if msg:
            errors.append(f"{f.relative_to(root)}: {msg}")

    loc_keys, loc_problems = load_loc(root)
    errors += loc_problems

    ab = ab_path(args[args.index("--ab") + 1] if "--ab" in args else None)
    if ab:
        loc_keys |= load_loc(ab)[0]

    if "--stub" in args:
        missing = [k for _, _, k in referenced_keys(root, files) if k not in loc_keys]
        for k in dict.fromkeys(missing):
            print(f' {k}: "TODO"')
        return

    verbose = "--verbose" in args or ab is not None or only is not None
    per_file = {}
    for rel, line, key in referenced_keys(root, files):
        if key not in loc_keys:
            per_file[rel] = per_file.get(rel, 0) + 1
            if verbose:
                where = "ABA or base AB (may be vanilla EU4)" if ab else "ABA localisation (may exist in base AB)"
                warnings.append(f"{rel}:{line}: loc key '{key}' not found in {where}")
    if not verbose:
        for rel, n in sorted(per_file.items(), key=lambda x: -x[1]):
            warnings.append(f"{rel}: {n} loc keys not found in ABA localisation")
        if per_file:
            print("NOTE    pass --ab <Ante Bellum folder> (or set AB_PATH) to also search base AB, "
                  "or --verbose for every key\n")

    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    print(f"\n{len(files)} script files checked: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
