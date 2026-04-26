import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from unpdf.converter import convert_pdf, ConversionResult

@patch("unpdf.converter.pymupdf4llm.to_markdown")
@patch("unpdf.converter.fitz.open")
def test_convert_pdf_success(mock_fitz_open, mock_to_markdown, tmp_path: Path):
    mock_to_markdown.return_value = "# Markdown Content"
    mock_doc = MagicMock()
    mock_doc.needs_pass = False
    mock_fitz_open.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)
    
    assert result == ConversionResult.SUCCESS
    assert output_md.read_text(encoding="utf-8") == "# Markdown Content"

@patch("unpdf.converter.fitz.open")
def test_convert_pdf_existing_skip(mock_fitz_open, tmp_path: Path):
    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()
    output_md.touch() # exists

    result = convert_pdf(input_pdf, output_md, force=False)
    
    assert result == ConversionResult.SKIPPED
    mock_fitz_open.assert_not_called()

@patch("unpdf.converter.pymupdf4llm.to_markdown")
@patch("unpdf.converter.fitz.open")
def test_convert_pdf_existing_force(mock_fitz_open, mock_to_markdown, tmp_path: Path):
    mock_to_markdown.return_value = "# New Content"
    mock_doc = MagicMock()
    mock_doc.needs_pass = False
    mock_fitz_open.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()
    output_md.write_text("Old Content")

    result = convert_pdf(input_pdf, output_md, force=True)
    
    assert result == ConversionResult.SUCCESS
    assert output_md.read_text(encoding="utf-8") == "# New Content"

@patch("unpdf.converter.fitz.open")
def test_convert_pdf_encrypted_skip(mock_fitz_open, tmp_path: Path):
    mock_doc = MagicMock()
    mock_doc.needs_pass = True
    mock_fitz_open.return_value = mock_doc

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)
    
    assert result == ConversionResult.SKIPPED
    assert not output_md.exists()

@patch("unpdf.converter.fitz.open")
def test_convert_pdf_corrupt(mock_fitz_open, tmp_path: Path):
    mock_fitz_open.side_effect = Exception("Corrupt PDF")

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)
    
    assert result == ConversionResult.SKIPPED
    assert not output_md.exists()
    
@patch("unpdf.converter.fitz.open")
@patch("unpdf.converter.pymupdf4llm.to_markdown")
def test_convert_pdf_error(mock_to_markdown, mock_fitz_open, tmp_path: Path):
    mock_doc = MagicMock()
    mock_doc.needs_pass = False
    mock_fitz_open.return_value = mock_doc
    mock_to_markdown.side_effect = Exception("Conversion Error")

    input_pdf = tmp_path / "in.pdf"
    output_md = tmp_path / "out.md"
    input_pdf.touch()

    result = convert_pdf(input_pdf, output_md, force=False)
    
    assert result == ConversionResult.ERROR
    assert not output_md.exists()
