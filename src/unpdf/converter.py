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
            f"Skipping existing output file: {output_file.name} (use --force to overwrite)"
        )
        return ConversionResult.SKIPPED

    with pymupdf.Document(input_file) as doc:
        if doc.is_encrypted:
            logger.warning(f"Skipping encrypted PDF: {input_file.name}")
            return ConversionResult.SKIPPED

        try:
            md_text = pymupdf4llm.to_markdown(doc)

            output_file.parent.mkdir(parents=True, exist_ok=True)

            output_file.write_text(md_text, encoding="utf-8")
            return ConversionResult.SUCCESS

        except PermissionError as e:
            logger.error(f"Permission denied writing to {output_file.parent}: {e}")
            return ConversionResult.ERROR
        except OSError as e:
            logger.error(f"File system error: {e}")
            return ConversionResult.ERROR
        except Exception as e:
            logger.error(f"Failed to convert {input_file.name}: {e}")
            return ConversionResult.ERROR
