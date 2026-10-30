# fixproof walkthrough

A static replay of three tabletop dry runs of the fixproof Skill on the fictional library in `../testdata/home-library/`. It replays recorded transcripts (`transcripts/`); it is not NAS runtime footage.

Scenarios: A (dishwasher E15, covered, claim saved), C (fridge, Unclear serial), E (warranty sweep).

Run it:

    python3 build.py && python3 -m http.server 8000
    open http://127.0.0.1:8000/   (or open index.html directly, it works from file://)

`?s=A&step=all` renders a whole scenario at once. `python3 test_build.py` checks the generated data. `python3 e2e_check.py OUT_DIR` clicks through all three scenarios in headless Chromium and saves screenshots to `OUT_DIR`.
