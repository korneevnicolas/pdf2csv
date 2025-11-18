"""
Test pypdf library for PDF to CSV conversion
Note: pypdf (formerly PyPDF2) is primarily for text extraction, not table extraction
"""
import time
import csv
import re

def test_pypdf():
    """Test pypdf library"""
    print("\n" + "="*80)
    print("TESTING: pypdf (formerly PyPDF2)")
    print("="*80)
    print("Note: pypdf is primarily for text extraction, not specialized for tables")

    pdf_file = "sample_table.pdf"
    output_csv = "output_pypdf.csv"

    try:
        from pypdf import PdfReader

        start_time = time.time()

        # Open PDF
        reader = PdfReader(pdf_file)
        print(f"✓ PDF has {len(reader.pages)} page(s)")

        all_text = []

        # Extract text from each page
        for page_num, page in enumerate(reader.pages, 1):
            print(f"\n[Page {page_num}]")
            text = page.extract_text()
            print(f"✓ Extracted {len(text)} characters")
            print(f"\nExtracted text preview:")
            print(text[:500])
            all_text.append(text)

        # Try to parse table from extracted text
        # This is very basic and won't work well for complex tables
        print("\n[Attempting basic table parsing from text]")

        lines = all_text[0].split('\n')
        table_data = []

        for line in lines:
            # Try to split by multiple spaces or tabs
            if line.strip():
                # Simple heuristic: split by 2+ spaces
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) > 1:
                    table_data.append(parts)

        print(f"✓ Parsed {len(table_data)} potential table rows")
        print("\nParsed data preview:")
        for i, row in enumerate(table_data[:5]):
            print(f"Row {i+1}: {row}")

        # Save to CSV
        if table_data:
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(table_data)
            print(f"\n✓ Saved to {output_csv}")

        elapsed_time = time.time() - start_time

        # Results summary
        print("\n" + "-"*80)
        print("RESULTS SUMMARY:")
        print(f"✓ Success: Partial (text extraction works, table parsing is basic)")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Text extracted: Yes")
        print(f"✓ Table structure: Poorly preserved")
        print(f"✓ Output file: {output_csv}")
        print(f"✓ Rows extracted: {len(table_data)}")
        print("\nLIMITATIONS:")
        print("  - pypdf is not designed for table extraction")
        print("  - Table structure is lost in text extraction")
        print("  - Manual parsing required and often unreliable")
        print("  - Better suited for simple text extraction tasks")

        return {
            'success': True,
            'quality_score': 3,  # Low score due to poor table structure preservation
            'time': elapsed_time,
            'tables_found': len(table_data) if table_data else 0,
            'errors': None,
            'note': 'Not suitable for table extraction'
        }

    except ImportError as e:
        print(f"\n✗ pypdf not installed: {str(e)}")
        return {
            'success': False,
            'quality_score': 0,
            'time': 0,
            'tables_found': 0,
            'errors': str(e)
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
    result = test_pypdf()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
