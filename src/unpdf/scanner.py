from pathlib import Path
from typing import Iterator

def scan_folder(input_path: Path, recurse: bool) -> Iterator[Path]:
    """
    Yields PDF files in the given path.
    If input_path is a file, yields it if it's a PDF.
    If input_path is a directory, yields PDFs based on recurse flag.
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
    if input_root == input_file or input_root.suffix.lower() == ".pdf":
        # Single file case
        return output_dir / input_file.with_suffix(".md").name

    # Folder case
    try:
        relative_path = input_file.relative_to(input_root)
    except ValueError:
        # Fallback if somehow not relative
        relative_path = Path(input_file.name)
        
    return output_dir / relative_path.with_suffix(".md")
