#!/usr/bin/env python3
"""Check a skill folder and zip it, keeping each file's real modified time.

Usage: package_skill.py <skill_dir> <out.zip>
"""
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_skill import check  # noqa: E402

def build(root, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or any(part.startswith(".") for part in path.relative_to(root).parts):
                continue
            mtime = time.localtime(path.stat().st_mtime)[:6]
            info = zipfile.ZipInfo(f"{root.name}/{path.relative_to(root).as_posix()}", mtime)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    root, out = Path(argv[1]).resolve(), Path(argv[2])
    rep = check(root)
    for level, code, file, line, msg in rep.items:
        print(f"{level} {code} {file}:{line} {msg}")
    if rep.errors:
        print(f"refusing to package: {rep.errors} errors", file=sys.stderr)
        return 1
    build(root, out)
    print(f"{out} {out.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
