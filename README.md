# unpdf

`unpdf` is a minimalist command-line utility designed to convert PDF documents into Markdown format, optimized for use with LLMs (Large Language Models). It leverages the power of `pymupdf4llm` to extract text, tables, and images while preserving the document structure.

## Features

- **Batch Processing**: Convert single files or entire directories.
- **Directory Preservation**: Recursively scans folders and mirrors the input structure in the output directory.
- **Smart Skip**: Automatically skips existing output files unless forced to overwrite.
- **Error Handling**: Gracefully handles encrypted or corrupt PDFs by logging warnings and continuing the batch.

## Technology Stack

- **Language**: Python 3.13+
- **PDF Engine**: [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm)
- **CLI**: Standard `argparse`

## Installation

### Prerequisites

- Python 3.13 or higher.

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd unpdf
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```

## Usage

```text
usage: unpdf [-h] INPUT -o DIR [--recurse] [--force] [--version]

positional arguments:
  INPUT                  PDF file or folder containing PDFs

options:
  -o DIR, --output DIR    Output folder (required)
  --recurse               Recursively scan subfolders
  --force                 Overwrite existing output files
  --version               Show version information and exit
```

### Examples

**Convert a single file:**
```bash
unpdf document.pdf -o ./output
```

**Convert an entire folder recursively:**
```bash
unpdf ./docs -o ./markdown_docs --recurse
```

## Project Structure

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

## Testing

Run the test suite using `pytest`:

```bash
pytest tests/
```

## Code Quality

This project uses several tools to maintain code quality:

```bash
black src/ tests/          # Format code
mypy src/ tests/          # Type checking
bandit -r src/ tests/      # Security analysis
```

## CI/CD

GitHub Actions automatically runs tests and linting on push and pull requests.

## Packaging

The project is designed to be packaged into a standalone executable using PyInstaller:

```bash
pyinstaller --onefile --console --clean --collect-all pymupdf --name unpdf src/unpdf/__main__.py
```