# PDF to CSV Converter

A comprehensive Python solution for extracting tables from PDF files and converting them to CSV format.

## Quick Start

```bash
# Install dependencies
pip install pdfplumber

# Convert PDF to CSV
python pdf2csv.py input.pdf output.csv
```

## Features

- ⚡ **Fast**: Processes PDFs in milliseconds
- 🎯 **Accurate**: 94.4% data completeness on test data
- 🔧 **Easy**: No external dependencies (pure Python)
- 📊 **Flexible**: Handle multiple tables and pages
- 🐍 **Production-ready**: Error handling and command-line interface

## Installation

```bash
# Basic installation (recommended)
pip install pdfplumber

# For maximum accuracy (requires ghostscript)
pip install camelot-py opencv-python-headless
sudo apt-get install ghostscript  # Linux
# brew install ghostscript  # macOS
```

## Usage

### Command Line

```bash
# Basic usage - convert PDF to CSV
python pdf2csv.py sample.pdf

# Specify output file
python pdf2csv.py sample.pdf output.csv

# Save each table separately
python pdf2csv.py sample.pdf --all-tables

# Process specific pages (0-indexed)
python pdf2csv.py sample.pdf --pages 0 2 4

# Quiet mode
python pdf2csv.py sample.pdf --quiet
```

### Python API

```python
from pdf2csv import pdf_to_csv

# Simple conversion
metadata = pdf_to_csv('input.pdf', 'output.csv')
print(f"Extracted {metadata['tables_found']} tables")

# Save each table separately
metadata = pdf_to_csv('input.pdf', all_tables=True)

# Process specific pages only
metadata = pdf_to_csv('input.pdf', pages=[0, 1, 2])
```

## Library Comparison

We tested 6 different Python libraries for PDF table extraction. See [ANALYSIS.md](ANALYSIS.md) for detailed comparison.

### Summary

| Library | Speed | Accuracy | Dependencies | Score |
|---------|-------|----------|--------------|-------|
| **pdfplumber** ⭐ | 0.05s | 94.4% | None | 9/10 |
| **camelot-py** | 0.79s | 100% | ghostscript | 10/10 |
| **pymupdf** | 0.05s | 94.4% | None | 9/10 |
| **tabula-py** | 2.74s | 93.9% | Java | 8/10 |
| **pypdf** | 0.01s | Poor | None | 2/10 |
| **pdfminer** | 0.07s | Poor | None | 3/10 |

### Recommendation

**Use pdfplumber** (default) for:
- 95% of use cases
- Best balance of speed, accuracy, and ease of use
- No external dependencies

**Use camelot-py** when:
- Maximum accuracy is critical (100%)
- You can handle the ghostscript dependency
- Slightly slower speed is acceptable

## Test Results

All test scripts are included:
- `test_tabula.py` - Tests tabula-py library
- `test_camelot.py` - Tests camelot-py library
- `test_pdfplumber.py` - Tests pdfplumber library (recommended)
- `test_pypdf.py` - Tests pypdf library
- `test_pdfminer.py` - Tests pdfminer.six library
- `test_pymupdf.py` - Tests pymupdf (fitz) library

Run any test:
```bash
python test_pdfplumber.py
```

## Sample Data

A sample PDF with a sales report table is included (`sample_table.pdf`) for testing.

To regenerate the sample PDF:
```bash
python create_sample_pdf.py
```

## Advanced Usage

### Custom Table Settings

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]

    # Custom table extraction settings
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_tolerance": 3,
    }

    tables = page.extract_tables(table_settings=table_settings)
```

### Using Camelot for Maximum Accuracy

```python
import camelot

# Lattice mode for bordered tables
tables = camelot.read_pdf("input.pdf", flavor='lattice', pages='all')

for table in tables:
    print(f"Accuracy: {table.accuracy}%")
    table.to_csv("output.csv")
```

## Common Issues

### No Tables Found

If no tables are extracted:
1. Check if the PDF contains actual tables (not images of tables)
2. Try different table extraction settings
3. Use camelot-py for complex tables
4. Consider OCR if tables are in images (use `pytesseract`)

### Poor Extraction Quality

If extraction quality is poor:
1. Try camelot-py for better accuracy
2. Adjust table_settings parameters
3. Use lattice mode for bordered tables
4. Use stream mode for borderless tables

### Installation Issues

If you encounter dependency issues:
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install pdfplumber
```

## Performance Tips

1. **For speed**: Use pdfplumber or pymupdf (0.05s)
2. **For accuracy**: Use camelot-py (100% accuracy)
3. **For large PDFs**: Process pages in batches
4. **For multiple PDFs**: Use multiprocessing

## Files

- `pdf2csv.py` - Main production-ready converter (recommended)
- `ANALYSIS.md` - Comprehensive library comparison and analysis
- `sample_table.pdf` - Sample PDF for testing
- `create_sample_pdf.py` - Script to generate sample PDF
- `test_*.py` - Individual library test scripts
- Output files: `output_*.csv` - Test results from each library

## Requirements

Minimum (pdfplumber only):
```
pdfplumber>=0.9.0
```

All libraries tested:
```
pdfplumber>=0.9.0
camelot-py>=0.11.0
opencv-python-headless>=4.5.0
tabula-py>=2.5.0
pypdf>=3.0.0
pdfminer.six>=20221105
pymupdf>=1.23.0
reportlab>=4.0.0  # For creating sample PDFs
```

## License

This project is provided as-is for educational and commercial use.

## Contributing

Contributions are welcome! Areas for improvement:
- Support for image-based tables (OCR)
- Better handling of merged cells
- Table structure detection improvements
- More test cases with various PDF types

## Acknowledgments

This project compares and benchmarks the following excellent libraries:
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [camelot](https://github.com/camelot-dev/camelot)
- [tabula-py](https://github.com/chezou/tabula-py)
- [pypdf](https://github.com/py-pdf/pypdf)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
