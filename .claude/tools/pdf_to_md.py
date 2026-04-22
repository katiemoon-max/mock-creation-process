"""Convert past-paper / mark-scheme / examiner-report PDFs to markdown using pymupdf4llm.

Output location: same folder as source, with .md extension. Filenames use human-readable
form: `Paper{N}-Question-{YEAR}.md`, `Paper{N}-MarkScheme-{YEAR}.md`,
`Paper{N}-ExaminerReport-{YEAR}.md`.

This script is subject/level/course-agnostic — it adapts to any exam board whose PDF
filenames match a consistent pattern. Configure the following to match your board:

  1. SOURCE_DIR          — where the PDFs live
  2. FILENAME_RE         — regex capturing (paper, code, year) from the PDF filename
  3. CODE_LABEL          — maps the board's file-code shorthand to human labels

Example configurations for common boards:

  Edexcel A Level Physics 9PH0 (filenames like `9PH0_01_que_20240613.pdf`):
      FILENAME_RE = re.compile(
          r"^(?:9PH0|9ph0)[_-](0[123])[_-](que|msc|rms|pef)[_-](\\d{4})\\d{4}\\.pdf$"
      )
      CODE_LABEL = {"que": "Question", "msc": "MarkScheme", "rms": "MarkScheme", "pef": "ExaminerReport"}

  AQA A Level Biology 7402 (filenames like `AQA-74021-QP-JUN22.PDF`):
      FILENAME_RE = re.compile(
          r"^AQA[-_]7402(\\d)[-_](QP|MS|INS)[-_]([A-Z]{3}\\d{2})\\.(pdf|PDF)$"
      )
      CODE_LABEL = {"QP": "Question", "MS": "MarkScheme", "INS": "Insert"}

Usage:
  python pdf_to_md.py              # convert all PDFs in SOURCE_DIR
  python pdf_to_md.py 01           # convert only Paper 1 PDFs
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf4llm

# --- Configure for your course --------------------------------------------------

SOURCE_DIR = Path(r"{{SOURCE_DIR}}")  # e.g. r"C:/Users/you/Documents/.../Spec Vault/{board}/{level}"

# Capture groups, in order: (paper, code, year)
FILENAME_RE = re.compile(
    r"^(?:9PH0|9ph0)[_-](0[123])[_-](que|msc|rms|pef)[_-](\d{4})\d{4}\.pdf$"
)

# Map the code group to a human-readable label for the output filename
CODE_LABEL = {
    "que": "Question",
    "msc": "MarkScheme",       # combined / long-form (multi-year)
    "rms": "MarkScheme",       # single-year
    "pef": "ExaminerReport",
}

# ------------------------------------------------------------------------------


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

        # Combined mark-scheme PDFs (multi-year) keep year in filename, with -combined suffix
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
