import logging
from pathlib import Path

from .scanner import scan_folder, get_output_path
from .converter import convert_pdf, ConversionResult

logger = logging.getLogger("unpdf")


def run_batch(input_root: Path, output_dir: Path, recurse: bool, force: bool) -> None:
    """
    Runs the conversion batch over the given input_root.

    Args:
        input_root: Path to a PDF file or directory containing PDFs.
        output_dir: Directory where Markdown files will be written.
        recurse: If True, scan subdirectories recursively.
        force: If True, overwrite existing output files.

    Note:
        A summary is logged only when more than one PDF is processed.
    """
    success_count = 0
    skip_count = 0
    error_count = 0
    total_found = 0

    for pdf_file in scan_folder(input_root, recurse):
        total_found += 1
        output_file = get_output_path(pdf_file, input_root, output_dir)

        result = convert_pdf(pdf_file, output_file, force)

        if result == ConversionResult.SUCCESS:
            success_count += 1
            logger.info(f"Converted: {pdf_file.name} -> {output_file}")
        elif result == ConversionResult.SKIPPED:
            skip_count += 1
            logger.warning(f"Skipped: {pdf_file.name}")
        elif result == ConversionResult.ERROR:
            error_count += 1
            logger.error(f"Error: {pdf_file.name}")

    if total_found > 1:
        error_string = f"{'error' if error_count == 1 else 'errors'}"
        logger.info(
            f"Summary: {total_found} found, {success_count} converted, {skip_count} skipped, {error_count} {error_string}."
        )
