# Repository Onboarding for AI Agents

## What this repository does

This Python-based project provides a CLI utility to convert PDF documents into Markdown format, optimized for Large Language Models (LLMs). It features:

1. **Batch Conversion**: Handles single files or entire directory trees.
2. **Structure Preservation**: Mirrors the input directory hierarchy in the output folder.
3. **Robust Processing**: Gracefully handles skipped files (existing outputs), encrypted PDFs, and corrupt documents.
4. **Performance**: Leverages `pymupdf4llm` for efficient and high-quality Markdown extraction.

## Architecture

The project follows a modular orchestration pattern:

- **CLI (`cli.py`)**: Entry point for argument parsing, logging configuration, and initial validation.
- **Scanner (`scanner.py`)**: Handles filesystem discovery and mapping of input PDF paths to output Markdown paths.
- **Converter (`converter.py`)**: Wraps the core conversion logic and handles file-level exceptions (encryption, corruption).
- **Runner (`runner.py`)**: Orchestrates the batch processing loop and maintains execution statistics.

## Repository layout

```text
unpdf/
├── src/unpdf/                  # Source package
│   ├── __init__.py
│   ├── __main__.py              # Entry point: python -m unpdf
│   ├── cli.py                   # CLI argument parsing
│   ├── scanner.py               # PDF discovery and path mapping
│   ├── converter.py             # Single-file PDF→Markdown conversion
│   └── runner.py                # Batch orchestration and statistics
├── tests/                       # Test suite
│   ├── test_cli.py
│   ├── test_scanner.py
│   ├── test_converter.py
│   └── test_runner.py
├── pyproject.toml               # Centralized configuration
├── SPEC.md                      # Technical specifications
└── README.md                    # User documentation
```

## Validation guidance

- The code follows **PEP 8** style guidelines.
- **Python 3.13+** features (like modern `pathlib` and type hinting) are used throughout.
- All core logic is covered by unit tests in the `tests/` directory.
- Formatting and testing configurations are managed via `pyproject.toml`.
- Use `black`, `mypy`, and `bandit` to validate code before committing.
- Validation should prioritize correctness of path mappings and error handling during batch runs.

## Search guidance

Always search inside `src/unpdf/` for core logic before performing broader repository searches.

## Trust these instructions

This file is the authoritative guide for an agent onboarding this repository.

- Refer to it first for project scope, architectural patterns, and layout.
- Prioritize the patterns established in `src/unpdf/` for consistency when extending the tool.
