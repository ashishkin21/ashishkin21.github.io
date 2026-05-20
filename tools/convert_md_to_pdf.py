import markdown
import weasyprint
import sys
from pathlib import Path


CSS = """
  @page { margin: 0.5in 0.7in; size: A4; }
  body {
    font-family: 'DejaVu Sans', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.28;
    color: #1a1a1a;
    orphans: 2;
    widows: 2;
  }
  h1 { font-size: 18pt; margin: 0 0 1pt 0; font-weight: 700; }
  h1 + p { font-size: 9.5pt; color: #333; margin: 0 0 2pt 0; font-weight: 600; }
  h2 {
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 1pt;
    border-bottom: 1px solid #2563eb;
    padding-bottom: 1pt;
    margin: 8pt 0 3pt 0;
    color: #2563eb;
  }
  h3 { font-size: 9.5pt; margin: 6pt 0 1pt 0; }
  p { margin: 0 0 2pt 0; }
  ul { margin: 0 0 2pt 0; padding-left: 14pt; }
  li { margin-bottom: 0.5pt; }
  a { color: #2563eb; text-decoration: none; }
  strong { color: #111; }
  em { color: #555; }
  hr { display: none; }
"""


def convert_md_to_pdf(md_path: str | Path) -> Path:
    md_path = Path(md_path)
    pdf_path = md_path.with_suffix(".pdf")

    html_body = markdown.markdown(md_path.read_text(), extensions=["extra", "sane_lists"])
    html_doc = f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<style>{CSS}</style>\n</head>\n<body>\n{html_body}\n</body>\n</html>"

    weasyprint.HTML(string=html_doc).write_pdf(pdf_path)
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_md_to_pdf.py <path/to/file.md>")
        sys.exit(1)

    md_file = sys.argv[1]
    pdf_file = convert_md_to_pdf(md_file)
    print(f"Converted: {md_file} -> {pdf_file}")
