# Technical Proposal: unpdf

## 1. Project Structure
```text
unpdf/
├── src/unpdf/                  # Source package
│   ├── __init__.py
│   ├── __main__.py              # Entry point: python -m unpdf
│   ├── cli.py                   # CLI argument parsing
│   ├── scanner.py               # PDF discovery and path mapping
│   ├── converter.py             # Single-file PDF→Markdown conversion
│   └── runner.py                # Batch orchestration and statistics collection
├── tests/
│   ├── test_scanner.py
│   ├── test_converter.py
│   └── test_runner.py
├── pyproject.toml
└── README.md
```

---

## 2. Technology Stack

| Component | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.13+ | User preference |
| CLI | argparse | Standard library, zero dependencies |
| PDF Conversion | pymupdf4llm | Evaluated and selected by user |
| Logging | logging | Standard library |
| Path Handling | pathlib.Path | Modern, cross-platform |

---

## 3. Dependencies (`pyproject.toml`)

```toml
[project]
name = "unpdf"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "pymupdf4llm",
]

[project.scripts]
unpdf = "unpdf.cli:main"

[project.optional-dependencies]
dev = [
    "pytest",
]
```

---

## 4. CLI Interface

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

---

## 5. Module Responsibilities

### `cli.py`
- Parse command-line arguments
- Configure logging
- Validate startup conditions
- Invoke batch runner
- Return appropriate exit code

### `scanner.py`
- Discover PDF files
- Support flat and recursive scanning
- Compute relative output paths
- Preserve directory structure

### `converter.py`
- Convert a single PDF to Markdown using `pymupdf4llm`
- Handle conversion-specific exceptions
- Write Markdown output

### `runner.py`
- Orchestrate batch processing
- Track statistics
- Handle skip logic
- Emit final summary

---

## 6. Core Algorithms

### 6.1 Folder Scanning

```python
scan_folder(path, recurse):
    if recurse:
        yield all .pdf files in path and subdirectories
    else:
        yield only top-level .pdf files
```

### 6.2 Folder Structure Preservation

```text
For each PDF:
  1. Compute relative path from input root
  2. Create destination subdirectory if needed
  3. Write .md file to matching output location

Only directories containing PDFs are created.
Empty directories are ignored.
```

### 6.3 Conversion Loop

```text
For each discovered PDF:
  1. Determine output path
  2. Skip if output exists (unless --force)
  3. Convert PDF to Markdown
  4. Write output file
  5. Record success, skip, or failure
```

---

## 7. Input Validation

| Scenario | Action | Exit Code |
|----------|--------|-----------|
| Input path does not exist | Print error and exit | `1` |
| Input file is not a PDF | Log warning and skip | `0` |
| Output directory does not exist | Create automatically | — |
| No PDFs found | Exit cleanly | `0` |

### Output Directory Safety

To prevent recursive self-processing:

- When `INPUT` is a directory and `--recurse` is enabled,
- the output directory **must not** be inside the input directory.

Invalid example:

```text
unpdf docs -o docs/output --recurse
```

This must terminate immediately with exit code `1`.

---

## 8. Error Handling

| Scenario | Action | Exit Code |
|----------|--------|-----------|
| Corrupt PDF | Log warning and skip | `0` |
| Password-protected PDF | Log warning and skip | `0` |
| Output already exists | Skip and log warning (unless `--force`) | `0` |
| Empty subfolder | Skip silently | `0` |
| Partial failures | Continue processing | `0` |
| Fatal startup error | Log error and exit | `1` |

---

## 9. Logging

- Log output is written to **stdout**.
- No log file is created.
- Default level: INFO.

Log format:
```python
LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)
```

Example:

```text
2025-01-15 10:23:01,452 - unpdf - WARNING - convert:42 - Skipping encrypted PDF: locked.
```

If more than one file is processed, emit a final INFO summary.

---

## 10. Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Fatal startup or configuration error |

---

## 12. Verification Plan

### Automated Tests

- `test_scanner.py`
  - Flat scanning
  - Recursive scanning
  - Empty directories
  - Non-PDF filtering

- `test_converter.py`
  - Successful conversion
  - Corrupt PDF handling
  - Password-protected PDF handling

- `test_runner.py`
  - Statistics tracking
  - Skip behavior
  - Force overwrite
  - Relative path preservation

### Manual Tests

- Single file conversion
- Flat folder conversion
- Recursive folder with mixed empty/non-empty subfolders
- Corrupt PDF logs a warning and skips conversion
- Existing output file logs a warning and skips conversion without `--force`
- Existing output file logs a warning and overwrites with `--force`
- Non-existent input path exits with code `1`
- Non-existent output directory is created automatically
- Output-inside-input rejection under `--recurse`
