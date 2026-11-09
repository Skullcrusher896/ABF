"""Print a navigable outline of a Clausewitz script file instead of reading it whole.

Usage: python -I outline.py FILE [--depth N] [--grep TEXT]

Shows top-level blocks with line ranges, the comment above each, and event ids / mission
slot+position. --depth 2 also lists second-level blocks (missions inside a mission group,
options inside events). --grep limits output to blocks whose header/comment/id contains TEXT.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from find import code_only  # noqa: E402


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    depth_max = 1
    grep = None
    if "--depth" in a:
        depth_max = int(a[a.index("--depth") + 1])
    if "--grep" in a:
        grep = a[a.index("--grep") + 1].lower()
    path = Path(a[0])
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    is_mission = "missions" in path.parts

    hdr = re.compile(r"^\s*([\w.:@\-]+)\s*=\s*\{")
    stack = []  # (name, start, depth, info)
    out = []
    depth = 0
    for i, l in enumerate(lines):
        c = code_only(l)
        m = hdr.match(c)
        if m and depth < depth_max:
            j = i - 1
            comment = ""
            while j >= 0 and lines[j].strip().startswith("#"):
                comment = lines[j].strip().lstrip("#").strip()
                j -= 1
            stack.append([m.group(1), i, depth, comment, []])
        if stack:
            s = re.match(r"^\s*(id|slot|position)\s*=\s*(\S+)", c)
            if s and depth in (stack[-1][2] + 1,):
                stack[-1][4].append(f"{s.group(1)}={s.group(2)}")
        depth = max(0, depth + c.count("{") - c.count("}"))
        while stack and depth <= stack[-1][2]:
            name, start, d, comment, info = stack.pop()
            out.append((start, i, d, name, comment, info))
    out.sort()
    shown = 0
    for start, end, d, name, comment, info in out:
        if d == 1 and not is_mission and name in ("trigger", "effect", "limit", "ai_chance",
                                                   "mean_time_to_happen", "immediate", "after"):
            continue
        text = f"{'  ' * d}{start+1}-{end+1}  {name}"
        if info:
            text += "  [" + " ".join(info) + "]"
        if comment:
            text += f"  # {comment}"
        if grep and grep not in text.lower():
            continue
        print(text)
        shown += 1
    print(f"\n{len(lines)} lines, {shown} blocks shown")


if __name__ == "__main__":
    main()
