import logging
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from unpdf.cli import main


def test_main_missing_input_path(tmp_path: Path):
    non_existent = tmp_path / "does_not_exist.pdf"
    sys.argv = ["unpdf", str(non_existent), "-o", str(tmp_path / "out")]

    result = main()

    assert result == 1


def test_main_output_inside_input_with_recurse(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = input_dir / "output"
    sys.argv = ["unpdf", str(input_dir), "-o", str(output_dir), "--recurse"]

    result = main()

    assert result == 1


def test_main_valid_invocation(tmp_path: Path):
    with patch("unpdf.cli.run_batch"):
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        input_file = input_dir / "test.pdf"
        input_file.touch()
        output_dir = tmp_path / "output"
        sys.argv = ["unpdf", str(input_dir), "-o", str(output_dir)]

        result = main()

        assert result == 0


def test_main_single_file_valid(tmp_path: Path):
    with patch("unpdf.cli.run_batch"):
        input_file = tmp_path / "test.pdf"
        input_file.touch()
        output_dir = tmp_path / "output"
        sys.argv = ["unpdf", str(input_file), "-o", str(output_dir)]

        result = main()

        assert result == 0


def test_main_recurse_flag_no_effect_on_file(tmp_path: Path, capsys):
    with patch("unpdf.cli.run_batch"):
        input_file = tmp_path / "test.pdf"
        input_file.touch()
        output_dir = tmp_path / "output"
        sys.argv = ["unpdf", str(input_file), "-o", str(output_dir), "--recurse"]

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "--recurse has no effect when INPUT is a single file." in captured.out


def test_main_run_batch_exception(tmp_path: Path):
    with patch("unpdf.cli.run_batch", side_effect=RuntimeError("batch failed")):
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        input_file = input_dir / "test.pdf"
        input_file.touch()
        output_dir = tmp_path / "output"
        sys.argv = ["unpdf", str(input_dir), "-o", str(output_dir)]

        result = main()

        assert result == 1
