# fixproof walkthrough

A small static replay of the validated tabletop dry runs of the fixproof Uliya Skill
(UGREEN AI NAS hackathon). It is a replay of recorded transcripts on a fictional
library, not NAS runtime footage. The Skill itself is just `SKILL.md` plus its references.

Scenarios: A (dishwasher E15, covered, claim saved), C (fridge, Unclear serial), E (warranty sweep).

Run it:

    python3 build.py && python3 -m http.server 8000
    open http://127.0.0.1:8000/   (or open index.html directly, it works from file://)

URL options: `?s=A&step=all` renders a whole scenario at once. `python3 test_build.py` checks the data.
