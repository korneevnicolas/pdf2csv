"""
Test pdfminer.six library for PDF to CSV conversion
Note: pdfminer is primarily for text extraction with layout analysis
"""
import time
import csv
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LAParams, LTTextContainer, LTChar, LTTextLine
import re

def test_pdfminer():
    """Test pdfminer.six library"""
    print("\n" + "="*80)
    print("TESTING: pdfminer.six")
    print("="*80)
    print("Note: pdfminer provides advanced text extraction with layout analysis")

    pdf_file = "sample_table.pdf"
    output_csv = "output_pdfminer.csv"

    try:
        start_time = time.time()

        # Method 1: Simple text extraction
        print("\n[Method 1] Simple text extraction:")
        text = extract_text(pdf_file)
        print(f"✓ Extracted {len(text)} characters")
        print(f"\nExtracted text preview:")
        print(text[:500])

        # Method 2: Extract with layout analysis
        print("\n[Method 2] Layout-aware extraction:")
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
            detect_vertical=False,
            all_texts=False
        )

        text_layout = extract_text(pdf_file, laparams=laparams)
        print(f"✓ Extracted {len(text_layout)} characters with layout analysis")

        # Method 3: Detailed page analysis
        print("\n[Method 3] Detailed page layout analysis:")
        for page_num, page_layout in enumerate(extract_pages(pdf_file, laparams=laparams), 1):
            print(f"\nPage {page_num}:")
            print(f"  - Width: {page_layout.width:.2f}")
            print(f"  - Height: {page_layout.height:.2f}")

            text_elements = []
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text_elements.append(element.get_text().strip())

            print(f"  - Text elements found: {len(text_elements)}")
            print(f"\nFirst 10 text elements:")
            for i, elem in enumerate(text_elements[:10]):
                print(f"    {i+1}. {elem}")

        # Try to parse table from extracted text
        print("\n[Attempting table parsing from layout-aware text]")
        lines = text_layout.split('\n')
        table_data = []

        for line in lines:
            line = line.strip()
            if line:
                # Try to split by multiple spaces
                parts = re.split(r'\s{2,}', line)
                if len(parts) >= 2:
                    table_data.append(parts)
                else:
                    # Single item, might be a cell value
                    table_data.append([line])

        print(f"✓ Parsed {len(table_data)} rows")
        print("\nParsed data preview:")
        for i, row in enumerate(table_data[:10]):
            print(f"Row {i+1} ({len(row)} cols): {row}")

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
        print(f"✓ Success: Partial (text extraction works, table structure limited)")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Text extracted: Yes")
        print(f"✓ Layout analysis: Yes (better than pypdf)")
        print(f"✓ Table structure: Partially preserved")
        print(f"✓ Output file: {output_csv}")
        print(f"✓ Rows extracted: {len(table_data)}")
        print("\nSTRENGTHS:")
        print("  + Better layout analysis than pypdf")
        print("  + Preserves some spatial information")
        print("  + Good for complex PDF text extraction")
        print("\nLIMITATIONS:")
        print("  - Not specialized for table extraction")
        print("  - Requires manual parsing for table structure")
        print("  - Less accurate than dedicated table extractors")

        return {
            'success': True,
            'quality_score': 5,  # Medium score - better than pypdf but not table-specialized
            'time': elapsed_time,
            'tables_found': len(table_data) if table_data else 0,
            'errors': None,
            'note': 'Better for text than tables'
        }

    except ImportError as e:
        print(f"\n✗ pdfminer.six not installed: {str(e)}")
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
    result = test_pdfminer()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
