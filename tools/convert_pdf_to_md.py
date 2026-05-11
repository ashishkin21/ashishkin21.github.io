import pymupdf
import sys
from pathlib import Path


def convert_pdf_to_md(pdf_path: str | Path) -> Path:
    pdf_path = Path(pdf_path)
    md_path = pdf_path.parent / (pdf_path.stem + "_pdf.md")

    doc = pymupdf.open(pdf_path)
    pages = [page.get_text() for page in doc]
    md_content = "\n\n".join(pages)

    md_path.write_text(md_content)
    return md_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf_to_md.py <path/to/file.pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    md_file = convert_pdf_to_md(pdf_file)
    print(f"Converted: {pdf_file} -> {md_file}")
