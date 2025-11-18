# pdf2csv

A systematic testing framework for evaluating multiple Python libraries for PDF to CSV table extraction.

## Overview

This repository provides a comprehensive testing framework to evaluate various Python libraries that can extract tabular data from PDF files and convert them to CSV format. The framework systematically tests each library and provides performance metrics and recommendations.

## Libraries Tested

1. **tabula-py** - Python wrapper for Tabula (Java-based), excellent for structured tables
2. **camelot-py** - Focuses specifically on table extraction with accuracy metrics
3. **pdfplumber** - Detailed control over PDF parsing with table detection
4. **PyMuPDF (fitz)** - Fast text extraction (requires manual table parsing)
5. **PyPDF2** - Basic PDF text extraction (requires manual table parsing)

## Installation

### Prerequisites

- Python 3.8 or higher
- Java Runtime Environment (required for tabula-py)
- System dependencies for camelot-py:
  - Ghostscript
  - Tkinter

### Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# On Ubuntu/Debian (for camelot-py):
sudo apt-get install python3-tk ghostscript

# On macOS:
brew install ghostscript tcl-tk
```

## Usage

### 1. Generate a Sample PDF

First, generate a sample PDF with a table for testing:

```bash
python generate_sample_pdf.py
```

This creates `sample_table.pdf` with sample sales data in a table format.

### 2. Run the Test Suite

Execute the systematic testing script:

```bash
python pdf_to_csv_test.py
```

The script will:
- Test each library systematically
- Extract tables/text from the PDF
- Save outputs to the `output/` directory
- Display performance metrics and recommendations

### 3. Review Results

Check the `output/` directory for extracted CSV files and text files from each library.

## Output

The test script generates:
- CSV files from successful table extraction
- Text files from basic text extraction methods
- Performance comparison report
- Recommendations based on your specific PDF

## Results Interpretation

The script provides:
- ✓ **Success** indicators for libraries that successfully extracted data
- ✗ **Failure** indicators for libraries that couldn't process the PDF
- **Execution time** for each library
- **Recommendations** based on:
  - Speed of extraction
  - Quality of table detection
  - Ease of use

## Recommendations by Use Case

- **Structured tables with clear borders**: Use `tabula-py` or `camelot-py`
- **Complex layouts or nested tables**: Use `pdfplumber`
- **Simple text extraction**: Use `PyPDF2` or `PyMuPDF`
- **High accuracy requirements**: Use `camelot-py` (provides accuracy metrics)

## Testing Your Own PDFs

To test with your own PDF files:

1. Replace `sample_table.pdf` with your PDF file
2. Update the `pdf_path` variable in `pdf_to_csv_test.py` if needed
3. Run `python pdf_to_csv_test.py`

## Troubleshooting

### Java Not Found (tabula-py)
```bash
# Install Java Runtime Environment
sudo apt-get install default-jre  # Ubuntu/Debian
brew install openjdk              # macOS
```

### Ghostscript Issues (camelot-py)
```bash
# Verify Ghostscript installation
gs --version

# If not installed:
sudo apt-get install ghostscript  # Ubuntu/Debian
brew install ghostscript          # macOS
```

## Project Structure

```
pdf2csv/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── generate_sample_pdf.py      # Script to generate test PDF
├── pdf_to_csv_test.py         # Main testing script
├── sample_table.pdf           # Generated test PDF (created by generate_sample_pdf.py)
└── output/                    # Output directory for extracted data (created by pdf_to_csv_test.py)
```

## Contributing

Feel free to add more libraries or improve the testing framework!

## License

MIT License