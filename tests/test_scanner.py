import pytest
from pathlib import Path
from unpdf.scanner import scan_folder, get_output_path


def test_scan_folder_flat(tmp_path: Path):
    (tmp_path / "1.pdf").touch()
    (tmp_path / "2.PDF").touch()
    (tmp_path / "3.txt").touch()

    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "4.pdf").touch()

    found = list(scan_folder(tmp_path, recurse=False))

    assert len(found) == 2
    assert tmp_path / "1.pdf" in found
    assert tmp_path / "2.PDF" in found


def test_scan_folder_recursive(tmp_path: Path):
    (tmp_path / "1.pdf").touch()
    (tmp_path / "3.txt").touch()

    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "2.pdf").touch()

    empty_sub = tmp_path / "empty"
    empty_sub.mkdir()

    found = list(scan_folder(tmp_path, recurse=True))

    assert len(found) == 2
    assert tmp_path / "1.pdf" in found
    assert sub / "2.pdf" in found


def test_scan_folder_single_file(tmp_path: Path):
    pdf = tmp_path / "1.pdf"
    pdf.touch()

    found = list(scan_folder(pdf, recurse=False))
    assert len(found) == 1
    assert found[0] == pdf


def test_scan_folder_single_non_pdf_file(tmp_path: Path):
    txt = tmp_path / "notes.txt"
    txt.touch()

    found = list(scan_folder(txt, recurse=False))
    assert len(found) == 0


def test_get_output_path_single_file(tmp_path: Path):
    input_file = tmp_path / "input.pdf"
    output_dir = tmp_path / "out"

    out_path = get_output_path(input_file, input_file, output_dir)
    assert out_path == output_dir / "input.md"


def test_get_output_path_folder(tmp_path: Path):
    input_root = tmp_path / "in"
    input_file = input_root / "sub" / "file.pdf"
    output_dir = tmp_path / "out"

    out_path = get_output_path(input_file, input_root, output_dir)
    assert out_path == output_dir / "sub" / "file.md"
