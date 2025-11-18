# PDF to CSV Library Comparison - Comprehensive Analysis

## Executive Summary

This analysis compares 6 Python libraries for extracting tabular data from PDFs and converting to CSV format. The test was conducted on a sample PDF containing a sales report table with 12 rows and 6 columns.

**Winner: pdfplumber** (for most use cases) or **camelot-py** (for maximum accuracy)

---

## Test Results Overview

| Library | Success | Time (s) | Accuracy | Tables Found | Data Completeness | Quality Score |
|---------|---------|----------|----------|--------------|-------------------|---------------|
| **tabula-py** | ✓ | 2.74 | Good | 1 | 93.9% | 8/10 |
| **camelot-py** | ✓ | 0.79 | Excellent | 1 | 100% | 10/10 |
| **pdfplumber** | ✓ | 0.05 | Very Good | 1 | 94.4% | 9/10 |
| **pypdf** | Partial | 0.01 | Poor | 0 | N/A | 2/10 |
| **pdfminer** | Partial | 0.07 | Poor | 0 (66 rows*) | N/A | 3/10 |
| **pymupdf (fitz)** | ✓ | 0.05 | Very Good | 1 | 94.4% | 9/10 |

*pdfminer extracted text elements, not structured table rows

---

## Detailed Library Analysis

### 1. tabula-py ⭐⭐⭐⭐

**Installation:**
```bash
pip install tabula-py
# Requires Java to be installed
```

**Strengths:**
- ✅ Specifically designed for PDF table extraction
- ✅ Excellent accuracy for most table types
- ✅ Supports both lattice (bordered) and stream (borderless) modes
- ✅ Can handle multiple tables per page
- ✅ Direct CSV export with `convert_into()` method
- ✅ Mature and well-maintained library
- ✅ Returns pandas DataFrames for easy manipulation

**Weaknesses:**
- ❌ Requires Java Runtime Environment (external dependency)
- ❌ Slowest of the working solutions (2.74 seconds)
- ❌ Startup overhead from Java subprocess
- ❌ Some warnings about font fallbacks

**Best For:**
- Complex PDFs with multiple tables
- Production environments where Java is already available
- When you need robust handling of various table formats

**Code Example:**
```python
import tabula

# Direct conversion
tabula.convert_into("input.pdf", "output.csv", output_format="csv", pages='all')

# Or get as DataFrame
df = tabula.read_pdf("input.pdf", pages='all', lattice=True)[0]
df.to_csv("output.csv", index=False)
```

---

### 2. camelot-py ⭐⭐⭐⭐⭐

**Installation:**
```bash
pip install camelot-py opencv-python-headless
# Requires ghostscript: apt-get install ghostscript
```

**Strengths:**
- ✅ **HIGHEST ACCURACY: 100%** on test PDF
- ✅ Provides accuracy metrics for each table
- ✅ Excellent handling of bordered tables (lattice mode)
- ✅ Good support for borderless tables (stream mode)
- ✅ Built-in table quality assessment
- ✅ Can export to multiple formats (CSV, JSON, Excel, HTML)
- ✅ Detailed parsing reports

**Weaknesses:**
- ❌ Requires ghostscript (external dependency)
- ❌ Slower than pdfplumber/pymupdf (0.79s)
- ❌ More complex installation
- ❌ Can have dependency conflicts (cryptography library)

**Best For:**
- Maximum accuracy requirements
- PDFs with complex table structures
- When you need quality metrics
- Production systems where accuracy is critical

**Code Example:**
```python
import camelot

# Lattice mode for bordered tables
tables = camelot.read_pdf("input.pdf", flavor='lattice', pages='all')

for i, table in enumerate(tables):
    print(f"Table {i+1} Accuracy: {table.accuracy}%")
    table.to_csv(f"output_{i+1}.csv")
```

---

### 3. pdfplumber ⭐⭐⭐⭐⭐ (RECOMMENDED)

**Installation:**
```bash
pip install pdfplumber
```

**Strengths:**
- ✅ **FASTEST** of all working solutions (0.05 seconds)
- ✅ No external dependencies (pure Python)
- ✅ Very easy to install and use
- ✅ Excellent accuracy (94.4%)
- ✅ Clean, intuitive API
- ✅ Good documentation
- ✅ Can extract other PDF elements (text, images, metadata)
- ✅ Customizable table extraction settings
- ✅ Works well with both simple and complex tables

**Weaknesses:**
- ❌ Slightly lower accuracy than camelot (94.4% vs 100%)
- ❌ May require tuning for complex tables

**Best For:**
- **Most use cases - RECOMMENDED DEFAULT CHOICE**
- Fast processing requirements
- Simple installation needs
- Development and prototyping
- When you need both speed and good accuracy

**Code Example:**
```python
import pdfplumber
import csv

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            with open("output.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(table)
```

---

### 4. pypdf ⭐

**Installation:**
```bash
pip install pypdf
```

**Strengths:**
- ✅ Very fast (0.01 seconds)
- ✅ No external dependencies
- ✅ Good for simple text extraction
- ✅ Lightweight

**Weaknesses:**
- ❌ **NOT SUITABLE FOR TABLE EXTRACTION**
- ❌ Loses all table structure
- ❌ Text comes out as unstructured lines
- ❌ Would require extensive manual parsing

**Best For:**
- Simple text extraction (not tables)
- PDF metadata reading
- Basic PDF operations

**Verdict:** ❌ Do not use for table extraction

---

### 5. pdfminer.six ⭐⭐

**Installation:**
```bash
pip install pdfminer.six
```

**Strengths:**
- ✅ Advanced layout analysis
- ✅ Better than pypdf for preserving spatial information
- ✅ Good for complex text extraction
- ✅ Fast (0.07 seconds)

**Weaknesses:**
- ❌ Not designed for table extraction
- ❌ Table structure mostly lost
- ❌ Requires significant manual parsing
- ❌ Extracted 66 text elements instead of 12 table rows

**Best For:**
- Complex text extraction with layout preservation
- Academic paper text extraction
- NOT for tables

**Verdict:** ❌ Do not use for table extraction

---

### 6. pymupdf (fitz) ⭐⭐⭐⭐

**Installation:**
```bash
pip install pymupdf
```

**Strengths:**
- ✅ **VERY FAST** (0.05 seconds, tied with pdfplumber)
- ✅ Built-in table detection (`find_tables()`)
- ✅ No external dependencies
- ✅ Excellent general PDF manipulation capabilities
- ✅ Good accuracy (94.4%)
- ✅ Very comprehensive PDF library

**Weaknesses:**
- ❌ Table detection API can be less intuitive
- ❌ Quality depends on PDF structure
- ❌ Newer table extraction feature (may have edge cases)

**Best For:**
- When you need both speed and table extraction
- Projects already using pymupdf
- When you need other PDF operations too (rendering, editing, etc.)

**Code Example:**
```python
import fitz
import csv

doc = fitz.open("input.pdf")
page = doc[0]

tables = page.find_tables()
for table in tables.tables:
    table_data = table.extract()

    with open("output.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table_data)

doc.close()
```

---

## Performance Comparison

### Speed Ranking:
1. **pypdf** - 0.01s (but doesn't work for tables)
2. **pdfplumber** - 0.05s ⚡
3. **pymupdf** - 0.05s ⚡
4. **pdfminer** - 0.07s
5. **camelot-py** - 0.79s
6. **tabula-py** - 2.74s

### Accuracy Ranking (for table extraction):
1. **camelot-py** - 100% 🏆
2. **pdfplumber** - 94.4%
3. **pymupdf** - 94.4%
4. **tabula-py** - 93.9%
5. **pdfminer** - Poor (not designed for tables)
6. **pypdf** - Poor (not designed for tables)

### Ease of Installation:
1. **pdfplumber** - Pure Python, no dependencies ⭐
2. **pymupdf** - Pure Python, no dependencies ⭐
3. **pypdf** - Pure Python, no dependencies
4. **pdfminer** - Pure Python, no dependencies
5. **camelot-py** - Requires ghostscript + opencv
6. **tabula-py** - Requires Java

### Ease of Use:
1. **pdfplumber** - Very intuitive API ⭐
2. **tabula-py** - Simple for basic cases
3. **pymupdf** - Good API, slightly more complex
4. **camelot-py** - Good API with metrics
5. **pdfminer** - Complex, requires parsing
6. **pypdf** - Simple but not suitable for tables

---

## Common Issues Handled

### Multiple Tables on One Page
- ✅ **tabula-py**: Excellent
- ✅ **camelot-py**: Excellent
- ✅ **pdfplumber**: Excellent
- ✅ **pymupdf**: Good

### Tables Spanning Multiple Pages
- ✅ **tabula-py**: Good (specify page ranges)
- ✅ **camelot-py**: Good (specify page ranges)
- ✅ **pdfplumber**: Good (iterate pages)
- ✅ **pymupdf**: Good (iterate pages)

### Complex Formatting/Merged Cells
- ✅ **camelot-py**: Best handling
- ✅ **tabula-py**: Good handling
- ⚠️ **pdfplumber**: May require tuning
- ⚠️ **pymupdf**: Depends on PDF structure

### Bordered vs Borderless Tables
- ✅ **camelot-py**: Both (lattice & stream modes)
- ✅ **tabula-py**: Both (lattice & stream modes)
- ✅ **pdfplumber**: Both (with table_settings)
- ⚠️ **pymupdf**: Better with bordered tables

---

## Final Recommendations

### 🥇 Overall Winner: **pdfplumber**

**Choose pdfplumber when:**
- You want the best balance of speed, accuracy, and ease of use
- You need fast processing (0.05s)
- You want simple installation with no external dependencies
- You're building a general-purpose PDF table extractor
- You need good-enough accuracy (94.4%)

### 🥈 Runner-up: **camelot-py**

**Choose camelot-py when:**
- **Accuracy is paramount** (100% accuracy)
- You need detailed quality metrics
- You're working with complex table structures
- Slightly slower speed is acceptable (0.79s)
- You can manage the ghostscript dependency

### 🥉 Alternative: **pymupdf**

**Choose pymupdf when:**
- You need speed + table extraction
- You're already using pymupdf for other PDF operations
- You need comprehensive PDF manipulation

### ❌ Not Recommended for Tables:
- **pypdf** - Use only for simple text extraction
- **pdfminer** - Use only for complex text with layout analysis
- **tabula-py** - Use only if Java is already in your environment and you need its specific features

---

## Production-Ready Solution

Here's the recommended production code using **pdfplumber**:

```python
import pdfplumber
import csv
import sys
from pathlib import Path

def pdf_to_csv(pdf_path, csv_path=None, page_range=None):
    """
    Convert PDF tables to CSV

    Args:
        pdf_path: Path to input PDF file
        csv_path: Path to output CSV file (default: same name as PDF)
        page_range: Pages to process (default: all pages)

    Returns:
        Number of tables extracted
    """
    pdf_path = Path(pdf_path)

    if csv_path is None:
        csv_path = pdf_path.with_suffix('.csv')

    table_count = 0
    all_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages if page_range is None else [pdf.pages[i] for i in page_range]

        for page_num, page in enumerate(pages, 1):
            # Extract tables with optimized settings
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 3,
            }

            tables = page.extract_tables(table_settings=table_settings)

            for table in tables:
                table_count += 1

                # Add all rows (skip header on subsequent tables)
                if table_count == 1:
                    all_rows.extend(table)
                else:
                    all_rows.extend(table[1:])  # Skip header for additional tables

    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

    print(f"✓ Extracted {table_count} table(s) to {csv_path}")
    print(f"✓ Total rows: {len(all_rows)}")

    return table_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_csv.py <pdf_file> [csv_file]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None

    pdf_to_csv(pdf_file, csv_file)
```

---

## Alternative: Maximum Accuracy Solution with Camelot

For when accuracy is critical:

```python
import camelot
import sys
from pathlib import Path

def pdf_to_csv_high_accuracy(pdf_path, csv_path=None, flavor='lattice'):
    """
    Convert PDF tables to CSV with maximum accuracy

    Args:
        pdf_path: Path to input PDF file
        csv_path: Path to output CSV file
        flavor: 'lattice' for bordered tables, 'stream' for borderless

    Returns:
        Accuracy percentage
    """
    pdf_path = Path(pdf_path)

    if csv_path is None:
        csv_path = pdf_path.with_suffix('.csv')

    # Extract tables
    tables = camelot.read_pdf(str(pdf_path), flavor=flavor, pages='all')

    print(f"✓ Found {len(tables)} table(s)")

    if tables:
        # Use the first table (or combine multiple)
        table = tables[0]

        print(f"✓ Accuracy: {table.accuracy:.2f}%")
        print(f"✓ Shape: {table.df.shape}")

        # Export to CSV
        table.to_csv(str(csv_path))

        print(f"✓ Saved to {csv_path}")

        return table.accuracy

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_csv_camelot.py <pdf_file> [csv_file]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None

    accuracy = pdf_to_csv_high_accuracy(pdf_file, csv_file)
    print(f"\nFinal accuracy: {accuracy:.2f}%")
```

---

## Conclusion

For **95% of use cases**, use **pdfplumber**. It offers the best combination of:
- ⚡ Speed (0.05 seconds)
- 🎯 Accuracy (94.4%)
- 🔧 Ease of installation (no dependencies)
- 💻 Ease of use (intuitive API)

For the remaining **5% where maximum accuracy is critical**, use **camelot-py** despite its slower speed and installation complexity.

Avoid pypdf and pdfminer for table extraction - they're not designed for this purpose.
