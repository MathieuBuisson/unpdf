import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .runner import run_batch

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        stream=sys.stdout
    )

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="unpdf",
        description="Convert PDF files to Markdown using pymupdf4llm."
    )
    parser.add_argument("INPUT", help="PDF file or folder containing PDFs")
    parser.add_argument("-o", "--output", dest="DIR", required=True, help="Output folder (required)")
    parser.add_argument("--recurse", action="store_true", help="Recursively scan subfolders")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}", help="Show version information and exit")
    
    args = parser.parse_args()

    setup_logging()

    input_path = Path(args.INPUT).resolve()
    output_dir = Path(args.DIR).resolve()

    if not input_path.exists():
        logger.error(f"Input path does not exist: {args.INPUT}")
        return 1

    if input_path.is_dir() and args.recurse:
        # Check if output directory is inside input directory
        try:
            output_dir.relative_to(input_path)
            logger.error("Output directory must not be inside the input directory when using --recurse.")
            return 1
        except ValueError:
            pass # Output directory is not inside input directory

    try:
        run_batch(input_path, output_dir, args.recurse, args.force)
        return 0
    except Exception as e:
        logger.error(f"Fatal error during batch processing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
