"""
Systematic PDF to CSV Conversion Testing Script

This script tests multiple Python libraries for extracting tabular data from PDFs
and converting them to CSV format. It evaluates each library's performance and
provides recommendations.
"""
import os
import sys
import time
import traceback
from typing import Dict, List, Tuple
import pandas as pd

# Results tracking
results = {}


def test_tabula_py(pdf_path: str, output_dir: str) -> Tuple[bool, str, float]:
    """Test tabula-py library."""
    start_time = time.time()
    try:
        import tabula
        
        # Read PDF into list of DataFrames
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        if not dfs:
            return False, "No tables found", time.time() - start_time
        
        # Save each table to CSV
        for i, df in enumerate(dfs):
            output_path = os.path.join(output_dir, f'tabula_table_{i+1}.csv')
            df.to_csv(output_path, index=False)
        
        elapsed = time.time() - start_time
        return True, f"Successfully extracted {len(dfs)} table(s)", elapsed
        
    except ImportError:
        return False, "Library not installed or Java not available", time.time() - start_time
    except Exception as e:
        return False, f"Error: {str(e)}", time.time() - start_time


def test_camelot_py(pdf_path: str, output_dir: str) -> Tuple[bool, str, float]:
    """Test camelot-py library."""
    start_time = time.time()
    try:
        import camelot
        
        # Read PDF tables
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        
        if not tables:
            # Try stream flavor if lattice doesn't work
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        
        if not tables:
            return False, "No tables found", time.time() - start_time
        
        # Save each table to CSV
        for i, table in enumerate(tables):
            output_path = os.path.join(output_dir, f'camelot_table_{i+1}.csv')
            table.df.to_csv(output_path, index=False)
        
        elapsed = time.time() - start_time
        accuracy = sum([t.accuracy for t in tables]) / len(tables) if tables else 0
        return True, f"Successfully extracted {len(tables)} table(s) with avg accuracy: {accuracy:.2f}", elapsed
        
    except ImportError:
        return False, "Library not installed or dependencies missing", time.time() - start_time
    except Exception as e:
        return False, f"Error: {str(e)}", time.time() - start_time


def test_pdfplumber(pdf_path: str, output_dir: str) -> Tuple[bool, str, float]:
    """Test pdfplumber library."""
    start_time = time.time()
    try:
        import pdfplumber
        
        tables_found = 0
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for i, table in enumerate(tables):
                    if table:
                        # Convert to DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        output_path = os.path.join(output_dir, f'pdfplumber_page{page_num+1}_table_{i+1}.csv')
                        df.to_csv(output_path, index=False)
                        tables_found += 1
        
        elapsed = time.time() - start_time
        if tables_found == 0:
            return False, "No tables found", elapsed
        return True, f"Successfully extracted {tables_found} table(s)", elapsed
        
    except ImportError:
        return False, "Library not installed", time.time() - start_time
    except Exception as e:
        return False, f"Error: {str(e)}", time.time() - start_time


def test_pymupdf(pdf_path: str, output_dir: str) -> Tuple[bool, str, float]:
    """Test PyMuPDF (fitz) library."""
    start_time = time.time()
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        tables_found = 0
        
        for page_num, page in enumerate(doc):
            # Extract text
            text = page.get_text()
            
            # Try to detect table-like structure
            lines = text.split('\n')
            if len(lines) > 1:
                # Simple heuristic: check if lines have similar structure
                output_path = os.path.join(output_dir, f'pymupdf_page{page_num+1}_text.txt')
                with open(output_path, 'w') as f:
                    f.write(text)
                tables_found += 1
        
        doc.close()
        elapsed = time.time() - start_time
        
        if tables_found == 0:
            return False, "No text content found", elapsed
        return True, f"Extracted text from {tables_found} page(s) (requires manual parsing)", elapsed
        
    except ImportError:
        return False, "Library not installed", time.time() - start_time
    except Exception as e:
        return False, f"Error: {str(e)}", time.time() - start_time


def test_pypdf2(pdf_path: str, output_dir: str) -> Tuple[bool, str, float]:
    """Test PyPDF2 library."""
    start_time = time.time()
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_path)
        text_found = 0
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            
            if text.strip():
                output_path = os.path.join(output_dir, f'pypdf2_page{page_num+1}_text.txt')
                with open(output_path, 'w') as f:
                    f.write(text)
                text_found += 1
        
        elapsed = time.time() - start_time
        
        if text_found == 0:
            return False, "No text content found", elapsed
        return True, f"Extracted text from {text_found} page(s) (requires manual parsing)", elapsed
        
    except ImportError:
        return False, "Library not installed", time.time() - start_time
    except Exception as e:
        return False, f"Error: {str(e)}", time.time() - start_time


def print_results(results: Dict):
    """Print formatted results."""
    print("\n" + "="*80)
    print("PDF TO CSV CONVERSION - TEST RESULTS")
    print("="*80 + "\n")
    
    successful = []
    failed = []
    
    for library, (success, message, elapsed) in results.items():
        if success:
            successful.append((library, message, elapsed))
        else:
            failed.append((library, message, elapsed))
    
    if successful:
        print("✓ SUCCESSFUL LIBRARIES:")
        print("-" * 80)
        for lib, msg, elapsed in successful:
            print(f"  {lib:20s} | {msg:40s} | Time: {elapsed:.3f}s")
        print()
    
    if failed:
        print("✗ FAILED LIBRARIES:")
        print("-" * 80)
        for lib, msg, elapsed in failed:
            print(f"  {lib:20s} | {msg:40s} | Time: {elapsed:.3f}s")
        print()
    
    print("="*80)
    print("\nRECOMMENDATIONS:")
    print("-" * 80)
    
    if successful:
        # Sort by elapsed time
        successful.sort(key=lambda x: x[2])
        fastest = successful[0]
        print(f"• Fastest: {fastest[0]} ({fastest[2]:.3f}s)")
        
        # Find best for table extraction
        table_libs = [s for s in successful if 'table' in s[1].lower()]
        if table_libs:
            print(f"• Best for tables: {table_libs[0][0]}")
        
        print(f"\n• For structured tables: Consider tabula-py or camelot-py")
        print(f"• For complex layouts: Consider pdfplumber")
        print(f"• For simple text extraction: PyPDF2 or PyMuPDF")
    else:
        print("• No libraries were successful. Check dependencies and PDF format.")
    
    print("="*80 + "\n")


def main():
    """Main function to test all libraries."""
    # Configuration
    pdf_path = "sample_table.pdf"
    output_dir = "output"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        print("Please run generate_sample_pdf.py first to create a sample PDF.")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("Starting systematic PDF to CSV conversion testing...")
    print(f"Input PDF: {pdf_path}")
    print(f"Output directory: {output_dir}\n")
    
    # Test each library
    libraries = [
        ("tabula-py", test_tabula_py),
        ("camelot-py", test_camelot_py),
        ("pdfplumber", test_pdfplumber),
        ("PyMuPDF", test_pymupdf),
        ("PyPDF2", test_pypdf2),
    ]
    
    for lib_name, test_func in libraries:
        print(f"Testing {lib_name}...", end=" ", flush=True)
        success, message, elapsed = test_func(pdf_path, output_dir)
        results[lib_name] = (success, message, elapsed)
        status = "✓" if success else "✗"
        print(f"{status} ({elapsed:.3f}s)")
    
    # Print results
    print_results(results)
    
    # List generated files
    print("Generated files in output directory:")
    print("-" * 80)
    if os.path.exists(output_dir):
        files = sorted(os.listdir(output_dir))
        for f in files:
            file_path = os.path.join(output_dir, f)
            size = os.path.getsize(file_path)
            print(f"  {f:40s} ({size:6d} bytes)")
    print()


if __name__ == "__main__":
    main()
