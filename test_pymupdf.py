"""
Test pymupdf (fitz) library for PDF to CSV conversion
"""
import fitz  # PyMuPDF
import time
import csv
import re

def test_pymupdf():
    """Test pymupdf (fitz) library"""
    print("\n" + "="*80)
    print("TESTING: pymupdf (fitz)")
    print("="*80)
    print("Note: pymupdf is very fast for text extraction and has table detection")

    pdf_file = "sample_table.pdf"
    output_csv = "output_pymupdf.csv"

    try:
        start_time = time.time()

        # Open PDF
        doc = fitz.open(pdf_file)
        print(f"✓ PDF has {len(doc)} page(s)")

        all_tables = []

        # Extract from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            print(f"\n[Page {page_num + 1}]")

            # Method 1: Simple text extraction
            text = page.get_text()
            print(f"✓ Extracted {len(text)} characters")
            print(f"\nText preview:")
            print(text[:300])

            # Method 2: Extract as dictionary (preserves more structure)
            print(f"\n[Text extraction as dictionary]")
            text_dict = page.get_text("dict")
            print(f"✓ Found {len(text_dict.get('blocks', []))} blocks")

            # Method 3: Try to find tables using text blocks
            print(f"\n[Attempting table detection]")
            try:
                tables = page.find_tables()
                table_list = tables.tables  # Get the actual list of tables
                print(f"✓ Found {len(table_list)} table(s)")

                for i, table in enumerate(table_list):
                    print(f"\nTable {i+1}:")
                    print(f"  - Rows: {table.row_count}")
                    print(f"  - Columns: {table.col_count}")
                    print(f"  - Bounding box: {table.bbox}")

                    # Extract table data
                    table_data = table.extract()
                    print(f"\nTable {i+1} preview (first 5 rows):")
                    for j, row in enumerate(table_data[:5]):
                        print(f"  Row {j+1}: {row}")

                    all_tables.append(table_data)
            except Exception as e:
                print(f"✗ Table detection error: {str(e)}")
                table_list = []

            # Fallback: If no tables found, try parsing from text
            if not table_list:
                print("\n[Fallback: Parsing from extracted text]")
                lines = text.split('\n')
                table_data = []

                for line in lines:
                    line = line.strip()
                    if line:
                        # Try to split by multiple spaces
                        parts = re.split(r'\s{2,}', line)
                        if len(parts) >= 2:
                            table_data.append(parts)

                if table_data:
                    print(f"✓ Parsed {len(table_data)} rows from text")
                    all_tables.append(table_data)

        # Save to CSV
        if all_tables:
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in all_tables[0]:
                    # Handle None values
                    cleaned_row = [cell if cell is not None else '' for cell in row]
                    writer.writerow(cleaned_row)
            print(f"\n✓ Saved to {output_csv}")

            # Calculate completeness
            total_cells = sum(len(row) for row in all_tables[0])
            non_empty_cells = sum(1 for row in all_tables[0] for cell in row if cell and str(cell).strip())
            completeness = (non_empty_cells / total_cells * 100) if total_cells > 0 else 0

        doc.close()
        elapsed_time = time.time() - start_time

        # Results summary
        print("\n" + "-"*80)
        print("RESULTS SUMMARY:")
        print(f"✓ Success: {'Yes' if all_tables else 'Partial'}")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Total tables found: {len(all_tables)}")
        print(f"✓ Output file: {output_csv}")

        if all_tables:
            print(f"✓ Data completeness: {completeness:.1f}%")
            print(f"✓ Rows extracted: {len(all_tables[0])}")
            print(f"✓ Columns extracted: {len(all_tables[0][0]) if all_tables[0] and len(all_tables[0]) > 0 else 0}")

        print("\nSTRENGTHS:")
        print("  + Very fast processing")
        print("  + Built-in table detection (find_tables)")
        print("  + Good text extraction capabilities")
        print("\nNOTE:")
        print("  - Table detection quality depends on PDF structure")
        print("  - Works best with well-formed tables")

        return {
            'success': len(all_tables) > 0,
            'quality_score': 0,
            'time': elapsed_time,
            'tables_found': len(all_tables),
            'errors': None
        }

    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'quality_score': 0,
            'time': 0,
            'tables_found': 0,
            'errors': str(e)
        }

if __name__ == "__main__":
    result = test_pymupdf()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
