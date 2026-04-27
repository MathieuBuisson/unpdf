import logging
from enum import Enum
from pathlib import Path

import pymupdf
import pymupdf4llm

logger = logging.getLogger("unpdf")


class ConversionResult(Enum):
    SUCCESS = "success"
    SKIPPED = "skipped"
    ERROR = "error"


def convert_pdf(
    input_file: Path, output_file: Path, force: bool = False
) -> ConversionResult:
    """
    Converts a single PDF to Markdown.
    """
    if output_file.exists() and not force:
        logger.warning(
            f"Skipping existing output: {output_file.name} (use --force to overwrite)"
        )
        return ConversionResult.SKIPPED

    doc = pymupdf.Document(str(input_file))
    if doc.is_encrypted:
        logger.warning(f"Skipping encrypted PDF: {input_file.name}")
        return ConversionResult.SKIPPED

    try:
        # Convert to Markdown
        md_text = pymupdf4llm.to_markdown(str(input_file))

        # Create destination subdirectory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write .md file
        output_file.write_text(md_text, encoding="utf-8")
        return ConversionResult.SUCCESS

    except Exception as e:
        logger.error(f"Failed to convert {input_file.name}: {e}")
        return ConversionResult.ERROR
