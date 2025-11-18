"""
EXAMPLE USAGE

This file demonstrates how to use the PDF to CSV testing framework.
"""

# Step 1: Install dependencies
# pip install -r requirements.txt

# Step 2: Generate a sample PDF (or use your own)
# python generate_sample_pdf.py

# Step 3: Run the systematic test
# python pdf_to_csv_test.py

# The script will test all libraries and output results like:
"""
Testing tabula-py... ✗ (0.000s)
Testing camelot-py... ✗ (0.000s)
Testing pdfplumber... ✓ (0.070s)
Testing PyMuPDF... ✓ (0.054s)
Testing PyPDF2... ✓ (0.026s)

RECOMMENDATIONS:
• Fastest: PyPDF2 (0.026s)
• Best for tables: pdfplumber

Generated files in output directory:
  pdfplumber_page1_table_1.csv
  pymupdf_page1_text.txt
  pypdf2_page1_text.txt
"""

# Step 4: Review the extracted files in the output/ directory
# The CSV file will contain the tabular data extracted from the PDF

# Example: Using the best library directly in your code
def extract_pdf_table_to_csv(pdf_path, output_csv):
    """
    Extract table from PDF using the best performing library (pdfplumber).
    """
    import pdfplumber
    import pandas as pd
    
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)
    
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        combined_df.to_csv(output_csv, index=False)
        print(f"Successfully saved to {output_csv}")
        return True
    else:
        print("No tables found in PDF")
        return False

# Example usage:
# extract_pdf_table_to_csv('sample_table.pdf', 'output.csv')
