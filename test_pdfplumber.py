"""
Test pdfplumber library for PDF to CSV conversion
"""
import pdfplumber
import time
import csv

def test_pdfplumber():
    """Test pdfplumber library"""
    print("\n" + "="*80)
    print("TESTING: pdfplumber")
    print("="*80)

    pdf_file = "sample_table.pdf"
    output_csv = "output_pdfplumber.csv"

    try:
        start_time = time.time()

        # Open PDF
        with pdfplumber.open(pdf_file) as pdf:
            print(f"✓ PDF has {len(pdf.pages)} page(s)")

            all_tables = []

            # Extract tables from each page
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n[Page {page_num}]")

                # Method 1: Extract table
                tables = page.extract_tables()
                print(f"✓ Found {len(tables)} table(s) on page {page_num}")

                for i, table in enumerate(tables):
                    print(f"\nTable {i+1}:")
                    print(f"  - Rows: {len(table)}")
                    print(f"  - Columns: {len(table[0]) if table else 0}")

                    # Display preview
                    print(f"\nTable {i+1} preview (first 5 rows):")
                    for row in table[:5]:
                        print(row)

                    all_tables.append(table)

                # Method 2: Extract table with settings
                print(f"\n[Alternative extraction with table_settings]")
                table_settings = {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "intersection_tolerance": 3,
                }
                tables_alt = page.extract_tables(table_settings=table_settings)
                print(f"✓ Found {len(tables_alt)} table(s) with custom settings")

            # Save to CSV (using first table)
            if all_tables:
                with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for row in all_tables[0]:
                        writer.writerow(row)
                print(f"\n✓ Saved to {output_csv}")

                # Calculate completeness
                total_cells = sum(len(row) for row in all_tables[0])
                non_empty_cells = sum(1 for row in all_tables[0] for cell in row if cell and cell.strip())
                completeness = (non_empty_cells / total_cells * 100) if total_cells > 0 else 0

        elapsed_time = time.time() - start_time

        # Results summary
        print("\n" + "-"*80)
        print("RESULTS SUMMARY:")
        print(f"✓ Success: Yes")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Total tables found: {len(all_tables)}")
        print(f"✓ Output file: {output_csv}")

        if all_tables:
            print(f"✓ Data completeness: {completeness:.1f}%")
            print(f"✓ Rows extracted: {len(all_tables[0])}")
            print(f"✓ Columns extracted: {len(all_tables[0][0]) if all_tables[0] else 0}")

        return {
            'success': True,
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
    result = test_pdfplumber()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
