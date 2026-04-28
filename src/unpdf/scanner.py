from pathlib import Path
from collections.abc import Iterator


def scan_folder(input_path: Path, recurse: bool) -> Iterator[Path]:
    """
    Scans for PDF files in the given path.

    Args:
        input_path: Path to a PDF file or directory containing PDFs.
        recurse: If True, scan subdirectories recursively.

    Yields:
        Path objects for each PDF file found.
    """
    if input_path.is_file():
        if input_path.suffix.lower() == ".pdf":
            yield input_path
        return

    if recurse:
        for p in input_path.rglob("*"):
            if p.is_file() and p.suffix.lower() == ".pdf":
                yield p
    else:
        for p in input_path.iterdir():
            if p.is_file() and p.suffix.lower() == ".pdf":
                yield p


def get_output_path(input_file: Path, input_root: Path, output_dir: Path) -> Path:
    """
    Computes the output Markdown path preserving relative structure.
    """
    if input_root.is_file() or input_root.suffix.lower() == ".pdf":
        # Single file case
        return output_dir / input_file.with_suffix(".md").name

    # Folder case
    try:
        relative_path = input_file.relative_to(input_root)
    except ValueError:
        # Defensive fallback - handles edge cases like symlinks or race conditions
        relative_path = Path(input_file.name)

    return output_dir / relative_path.with_suffix(".md")
