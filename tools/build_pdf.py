"""Render a Markdown proposal to a styled PDF.

Usage: .venv/bin/python project/tools/build_pdf.py submission/PROPOSAL.md submission/proposal.pdf
"""
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
@page { size: A4; margin: 16mm 17mm; @bottom-right { content: counter(page) " / " counter(pages); font-size: 8pt; color: #888; } }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 9.6pt; line-height: 1.42; color: #1d2230; }
h1 { font-size: 20pt; margin: 0 0 2pt; color: #0b7a4b; }
h1 + p { font-size: 11pt; color: #444; margin-top: 0; }
h2 { font-size: 12.5pt; color: #0b7a4b; border-bottom: 1.2pt solid #0b7a4b; padding-bottom: 2pt; margin: 13pt 0 5pt; }
h3 { font-size: 10.5pt; margin: 9pt 0 3pt; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0; font-size: 8.8pt; }
th, td { border: 0.6pt solid #c8ccd4; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #eaf5ef; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.4pt; background: #f2f3f5; padding: 0 2pt; }
pre { background: #f2f3f5; padding: 6pt; font-size: 8pt; white-space: pre-wrap; border-left: 2pt solid #0b7a4b; }
pre code { background: none; padding: 0; }
blockquote { margin: 5pt 0; padding: 4pt 9pt; background: #f6faf8; border-left: 3pt solid #0b7a4b; color: #333; }
ul, ol { margin: 3pt 0 3pt 14pt; padding: 0; }
li { margin: 1pt 0; }
img { max-width: 100%; }
"""


def main(src: str, dst: str) -> None:
    md_text = Path(src).read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    HTML(string=html, base_url=str(Path(src).parent.resolve())).write_pdf(dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
