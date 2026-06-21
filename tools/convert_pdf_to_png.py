from pathlib import Path

import fitz


def pdf_to_png(
    pdf_path: str | Path,
    output_dir: str | Path | None = None,
    dpi: int = 200,
) -> list[Path]:
    """Render each page of a PDF to a PNG image.

    Args:
        pdf_path: Path to the source PDF file.
        output_dir: Directory for output images. Defaults to the PDF's directory.
        dpi: Resolution of the output images. Default is 200.

    Returns:
        List of paths to the generated PNG files.
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir) if output_dir else pdf_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    doc = fitz.open(pdf_path)
    output_paths: list[Path] = []

    try:
        for page_number in range(len(doc)):
            page = doc[page_number]
            pix = page.get_pixmap(matrix=matrix)
            out_path = output_dir / f"{pdf_path.stem}_page_{page_number + 1}.png"
            pix.save(out_path)
            output_paths.append(out_path)
    finally:
        doc.close()

    return output_paths


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_to_png.py <path/to/file.pdf> [output_dir]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    for path in pdf_to_png(pdf_file, out_dir):
        print(path)
