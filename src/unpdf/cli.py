import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .runner import run_batch


def setup_logging() -> logging.Logger:
    """Configure root logging to stdout at INFO level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        stream=sys.stdout,
        force=True,
    )
    return logging.getLogger("unpdf")


def main() -> int:
    """Parse arguments, validate inputs, and run the batch conversion. Returns exit code."""
    parser = argparse.ArgumentParser(
        prog="unpdf", description="Convert PDF files to Markdown using pymupdf4llm."
    )
    parser.add_argument("INPUT", help="PDF file or folder containing PDFs")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        required=True,
        help="Output folder (required)",
    )
    parser.add_argument(
        "--recurse", action="store_true", help="Recursively scan subfolders"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing output files"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version information and exit",
    )

    logger = setup_logging()
    args = parser.parse_args()

    input_path = Path(args.INPUT).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_path.exists():
        logger.error(f"Input path does not exist: {args.INPUT}")
        return 1

    if input_path.is_file() and args.recurse:
        logger.warning("--recurse has no effect when INPUT is a single file.")

    if input_path.is_dir() and args.recurse:
        if output_dir.is_relative_to(input_path):
            logger.error(
                "Output directory must not be inside the input directory when using --recurse."
            )
            return 1

    try:
        run_batch(input_path, output_dir, args.recurse, args.force)
        return 0
    except Exception as e:
        logger.error(f"Fatal error during batch processing: {e}")
        return 1
