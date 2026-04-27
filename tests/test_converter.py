import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from unpdf.converter import convert_pdf, ConversionResult


@patch("unpdf.converter.pymupdf4llm.to_markdown")
@patch("unpdf.converter.pymupdf.Document")
def test_convert_pdf_success(mock_document, mock_to_markdown, tmp_path: Path):
    mock_to_markdown.return_value = "# Markdown Content"
    mock_doc = MagicMock()
    mock_doc.is_encrypted = False
    mock_document.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)

    assert result == ConversionResult.SUCCESS
    assert output_md.read_text(encoding="utf-8") == "# Markdown Content"


@patch("unpdf.converter.pymupdf.Document")
def test_convert_pdf_existing_skip(mock_document, tmp_path: Path):
    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()
    output_md.touch()  # exists

    result = convert_pdf(input_pdf, output_md, force=False)

    assert result == ConversionResult.SKIPPED
    mock_document.assert_not_called()


@patch("unpdf.converter.pymupdf4llm.to_markdown")
@patch("unpdf.converter.pymupdf.Document")
def test_convert_pdf_existing_force(mock_document, mock_to_markdown, tmp_path: Path):
    mock_to_markdown.return_value = "# New Content"
    mock_doc = MagicMock()
    mock_doc.is_encrypted = False
    mock_document.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()
    output_md.write_text("Old Content")

    result = convert_pdf(input_pdf, output_md, force=True)

    assert result == ConversionResult.SUCCESS
    assert output_md.read_text(encoding="utf-8") == "# New Content"


@patch("unpdf.converter.pymupdf.Document")
def test_convert_pdf_encrypted_skip(mock_document, tmp_path: Path):
    mock_doc = MagicMock()
    mock_doc.is_encrypted = True
    mock_document.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)

    assert result == ConversionResult.SKIPPED
    assert not output_md.exists()


@patch("unpdf.converter.pymupdf.Document")
def test_convert_pdf_corrupt(mock_document, tmp_path: Path):
    mock_doc = MagicMock()
    mock_doc.is_encrypted = False
    mock_document.return_value = mock_doc
    import pymupdf4llm

    with patch(
        "unpdf.converter.pymupdf4llm.to_markdown", side_effect=Exception("Corrupt PDF")
    ):
        input_pdf = tmp_path / "in.pdf"
        output_md = tmp_path / "out.md"
        input_pdf.touch()

        result = convert_pdf(input_pdf, output_md, force=False)

    assert result == ConversionResult.ERROR
    assert not output_md.exists()


@patch("unpdf.converter.pymupdf.Document")
@patch("unpdf.converter.pymupdf4llm.to_markdown")
def test_convert_pdf_error(mock_to_markdown, mock_document, tmp_path: Path):
    mock_doc = MagicMock()
    mock_doc.is_encrypted = False
    mock_document.return_value = mock_doc
    mock_to_markdown.side_effect = Exception("Conversion Error")

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)

    assert result == ConversionResult.ERROR
    assert not output_md.exists()
