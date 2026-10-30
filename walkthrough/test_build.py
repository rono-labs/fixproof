#!/usr/bin/env python3
"""Checks for data/scenarios.json. Run: python3 test_build.py (or pytest)."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE.parent / "testdata" / "home-library"


def load():
    subprocess.run([sys.executable, str(HERE / "build.py")], check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    return {s["id"]: s for s in json.loads((HERE / "data" / "scenarios.json").read_text(encoding="utf-8"))}


def test_all():
    d = load()
    assert len(d) == 3 and set(d) == {"A", "C", "E"}
    assert len(d["A"]["steps"]) == 13
    assert "Covered" in d["A"]["answer"] and "EPP-3Y-90417733" in d["A"]["answer"]
    assert "Unclear" in d["C"]["answer"] and "30847" in d["C"]["answer"] and "30647" in d["C"]["answer"]
    assert "2,527" in d["E"]["answer"]
    for s in d.values():
        assert s["prompt"] and s["steps"]
        for st in s["steps"]:
            assert st["agent"] and st["ask"] and st["result"]
            for f in st["files"]:
                assert (LIB / f).is_file(), f
    again = json.dumps(load(), sort_keys=True)
    assert again == json.dumps(d, sort_keys=True)  # deterministic
    for p in HERE.glob("data/*"):
        assert "—" not in p.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_all()
    print("ok")
