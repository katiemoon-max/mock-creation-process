"""Convert Edexcel A Level Physics PDFs to markdown using pymupdf4llm.

Output location: same folder as source, with .md extension. Filenames use human-readable
form: `Paper1-Question-2024.md`, `Paper1-MarkScheme-2024.md`, `Paper1-ExaminerReport-2024.md`.

File code legend (Edexcel):
  que = Question paper
  msc = Combined Mark Scheme (multiple years in one doc)
  rms = Reserved/Revised Mark Scheme (single year)
  pef = Principal Examiner Feedback (examiner report)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf4llm

SOURCE_DIR = Path(r"C:/Users/Katie Moon/Documents/Claude/03 - Resources/Spec Vault/Edexcel/A-Level")

CODE_LABEL = {
    "que": "Question",
    "msc": "MarkScheme",  # combined / long-form
    "rms": "MarkScheme",
    "pef": "ExaminerReport",
}

FILENAME_RE = re.compile(
    r"^(?:9PH0|9ph0)[_-](0[123])[_-](que|msc|rms|pef)[_-](\d{4})\d{4}\.pdf$"
)


def parse(name: str) -> tuple[str, str, str] | None:
    m = FILENAME_RE.match(name)
    if not m:
        return None
    paper, code, year = m.groups()
    return paper, code, year


def target_name(paper: str, code: str, year: str) -> str:
    label = CODE_LABEL[code]
    return f"Paper{int(paper)}-{label}-{year}.md"


def convert_one(pdf_path: Path, out_path: Path) -> int:
    md = pymupdf4llm.to_markdown(str(pdf_path))
    header = f"# {out_path.stem.replace('-', ' ')}\n\n_Source: {pdf_path.name}_\n\n---\n\n"
    out_path.write_text(header + md, encoding="utf-8")
    return len(md)


def main() -> None:
    only_paper = sys.argv[1] if len(sys.argv) > 1 else None  # e.g. "01"
    pdfs = sorted(SOURCE_DIR.glob("*.pdf"))
    converted = skipped = failed = 0

    for pdf in pdfs:
        parsed = parse(pdf.name)
        if parsed is None:
            print(f"SKIP (unrecognised): {pdf.name}")
            skipped += 1
            continue
        paper, code, year = parsed
        if only_paper and paper != only_paper:
            continue

        # Combined mark-scheme PDFs (msc) already cover multiple years; keep year in filename
        out_name = target_name(paper, code, year)
        if code == "msc":
            out_name = out_name.replace(".md", "-combined.md")
        out_path = SOURCE_DIR / out_name

        if out_path.exists() and out_path.stat().st_size > 1000:
            print(f"EXISTS: {out_name}")
            skipped += 1
            continue

        try:
            size = convert_one(pdf, out_path)
            print(f"OK ({size:>6} chars): {pdf.name} -> {out_name}")
            converted += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: {pdf.name} -- {exc}")
            failed += 1

    print(f"\nDone. Converted: {converted}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()
