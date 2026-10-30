#!/usr/bin/env python3
"""Parse the validated dry-run transcripts into data/scenarios.json and data/scenarios.js."""
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
VALIDATION = PROJECT / "validation"
LIBRARY = PROJECT / "testdata" / "home-library"
RUNS = [
    ("A", "dryrun-A.md", "Dishwasher shows E15"),
    ("C", "dryrun-C.md", "Fridge stopped cooling"),
    ("E", "dryrun-E.md", "Warranty sweep"),
]
ASK_MAX = 220
LINE_MAX = 260
PARENT_MAX = 520


def cut(text, limit):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


def library_files():
    return sorted(p.relative_to(LIBRARY).as_posix() for p in LIBRARY.rglob("*") if p.is_file())


def sections(text, prefix):
    """Split text on headings that start with prefix; returns list of (heading, body)."""
    parts = re.split(r"^(%s[^\n]*)\n" % re.escape(prefix), text, flags=re.M)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]


def parse_delegation(heading, body, files):
    agent = re.search(r"to ([\w-]+)", heading).group(1)
    lines = body.split("\n")
    ask_lines, result_lines, parent_lines = [], [], []
    mode = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("Instruction as sent"):
            mode = "ask"
            continue
        if s.startswith("Result ("):
            mode = "result"
            rest = s.split("):", 1)[1].strip() if "):" in s else ""
            if rest:
                result_lines.append(rest)
            continue
        if re.match(r"^(Parent|Arithmetic|Exclusions)\b", s):
            mode = "parent"
            parent_lines.append(re.sub(r"^Parent[^:]*:\s*", "", s))
            continue
        if not s:
            continue
        if mode == "ask" and s.startswith(">"):
            ask_lines.append(s.lstrip("> ").strip())
        elif mode == "result" and not s.startswith("(") and not s.startswith("```"):
            result_lines.append(re.sub(r"^-\s+", "", s))
        elif mode == "parent" and not s.startswith("```"):
            parent_lines.append(s)
    blob = body
    present = [f for f in files if f in blob]
    # drop files that are a substring of a longer matched path
    present = [f for f in present if not any(f != g and f in g for g in present)]
    return {
        "agent": agent,
        "ask": cut(" ".join(ask_lines), ASK_MAX),
        "result": [cut(l, LINE_MAX) for l in result_lines[:4]],
        "parent": cut(" ".join(parent_lines), PARENT_MAX),
        "files": present,
    }


def parse_run(sid, fname, title, files):
    text = (VALIDATION / fname).read_text(encoding="utf-8")
    h1 = re.search(r'^# Dry run \w+: "(.*)"\s*$', text, flags=re.M)
    prompt = h1.group(1)
    head = text.split("\n## ", 1)[0]
    m = re.search(r'Second user turn: "([^"]+)"', head)
    second = m.group(1) if m else None

    intake = re.search(r"^## Intake\n(.*?)(?=^## )", text, flags=re.M | re.S).group(1).strip()
    steps = []
    reply_idx = None
    body_start = text.index("\n## Step") if "\n## Step" in text else 0
    final_idx = text.index("## Final answer")
    sects = sections(text[body_start:final_idx] + "\n", "## ")
    for sh, sb in sects:
        pre = sb.split("### Delegation", 1)[0]
        draft = re.search(r"```\n(.*?)\n```", pre, flags=re.S)
        if "User reply" in pre and reply_idx is None:
            reply_idx = len(steps)
        if draft:
            draft_target = len(steps) - 1
        for dh, db in sections("\n" + sb, "### Delegation"):
            steps.append(parse_delegation(dh, db, files))
        if draft:
            steps[draft_target]["draft"] = draft.group(1)
    for s in steps:
        s.setdefault("draft", "")
    after = text[final_idx:]
    answer = re.search(r"```\n(.*?)\n```", after, flags=re.S).group(1)
    st = re.search(r"^Status: `(\w+)`(?:, (.*))?$", after, flags=re.M)
    dl = re.search(r"^Delegations: (\d+)(?: \((.*)\))?\.?$", after, flags=re.M)
    return {
        "id": sid,
        "title": title,
        "prompt": prompt,
        "intake": intake,
        "second_turn": second,
        "second_turn_before_step": reply_idx if second else None,
        "steps": steps,
        "answer": answer,
        "status": st.group(1),
        "saved": (st.group(2) or "").replace("saved to ", "") or None,
        "delegations": int(dl.group(1)),
        "delegation_detail": dl.group(2) or "",
    }


def main():
    files = library_files()
    scenarios = [parse_run(sid, f, t, files) for sid, f, t in RUNS]
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    (data / "scenarios.json").write_text(json.dumps(scenarios, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    js = "window.SCENARIOS = %s;\nwindow.LIBRARY = %s;\n" % (
        json.dumps(scenarios, indent=1, ensure_ascii=False), json.dumps(files, indent=1))
    (data / "scenarios.js").write_text(js, encoding="utf-8")
    used = sorted({f for sc in scenarios for s in sc["steps"] for f in s["files"] if f.lower().endswith(".jpg")})
    for f in used:
        dst = HERE / "assets" / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LIBRARY / f, dst)
    print("scenarios:", len(scenarios), "library files:", len(files), "photos copied:", len(used))


if __name__ == "__main__":
    main()
