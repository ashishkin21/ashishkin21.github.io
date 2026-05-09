import mammoth
import sys
from pathlib import Path


def convert_docx_to_md(docx_path: str | Path) -> Path:
    docx_path = Path(docx_path)
    md_path = docx_path.with_suffix(".md")

    with open(docx_path, "rb") as f:
        result = mammoth.convert_to_markdown(f)
        md_content = result.value

    md_path.write_text(md_content)
    return md_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_docx_to_md.py <path/to/file.docx>")
        sys.exit(1)

    docx_file = sys.argv[1]
    md_file = convert_docx_to_md(docx_file)
    print(f"Converted: {docx_file} -> {md_file}")
