import pytest
from pathlib import Path
from unittest.mock import patch, call
from unpdf.runner import run_batch
from unpdf.converter import ConversionResult


@patch("unpdf.runner.convert_pdf")
def test_run_batch(mock_convert_pdf, tmp_path: Path, caplog):
    # Setup files
    in_dir = tmp_path / "in"
    in_dir.mkdir()

    (in_dir / "1.pdf").touch()
    (in_dir / "2.pdf").touch()
    (in_dir / "3.pdf").touch()

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Mock responses: 1 success, 1 skipped, 1 error
    mock_convert_pdf.side_effect = [
        ConversionResult.SUCCESS,
        ConversionResult.SKIPPED,
        ConversionResult.ERROR,
    ]

    import logging

    with caplog.at_level(logging.INFO):
        run_batch(in_dir, out_dir, recurse=False, force=False)

    assert "Summary: 3 found, 1 converted, 1 skipped, 1 error." in caplog.text
    assert mock_convert_pdf.call_count == 3


@patch("unpdf.runner.convert_pdf")
def test_run_batch_empty(mock_convert_pdf, tmp_path: Path, caplog):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    out_dir = tmp_path / "out"

    import logging

    with caplog.at_level(logging.INFO):
        run_batch(in_dir, out_dir, recurse=False, force=False)

    assert mock_convert_pdf.call_count == 0


@patch("unpdf.runner.convert_pdf")
def test_run_batch_force_flag(mock_convert_pdf, tmp_path: Path):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    (in_dir / "doc.pdf").touch()

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    existing_output = out_dir / "doc.md"
    existing_output.touch()

    mock_convert_pdf.return_value = ConversionResult.SUCCESS

    run_batch(in_dir, out_dir, recurse=False, force=True)

    mock_convert_pdf.assert_called_once_with(in_dir / "doc.pdf", existing_output, True)


@patch("unpdf.runner.convert_pdf")
def test_run_batch_path_preservation(mock_convert_pdf, tmp_path: Path):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    sub_dir = in_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "doc.pdf").touch()

    out_dir = tmp_path / "out"

    mock_convert_pdf.return_value = ConversionResult.SUCCESS

    run_batch(in_dir, out_dir, recurse=True, force=False)

    expected_output = out_dir / "subdir" / "doc.md"
    mock_convert_pdf.assert_called_once_with(
        in_dir / "subdir" / "doc.pdf", expected_output, False
    )
