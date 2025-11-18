"""
Test camelot-py library for PDF to CSV conversion
"""
import time

def test_camelot():
    """Test camelot-py library"""
    print("\n" + "="*80)
    print("TESTING: camelot-py")
    print("="*80)

    pdf_file = "sample_table.pdf"
    output_csv = "output_camelot.csv"

    try:
        import camelot

        start_time = time.time()

        # Method 1: Using lattice mode (for tables with clear borders)
        print("\n[Method 1] Lattice mode (for bordered tables):")
        tables = camelot.read_pdf(pdf_file, flavor='lattice', pages='all')
        print(f"✓ Found {len(tables)} table(s)")

        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(f"  - Shape: {table.df.shape}")
            print(f"  - Parsing report: {table.parsing_report}")
            print(f"  - Accuracy: {table.accuracy:.2f}%")
            print(f"  - Whitespace: {table.whitespace:.2f}%")
            print(f"\nTable {i+1} preview:")
            print(table.df.head(10))

            # Save to CSV
            if i == 0:
                table.to_csv(output_csv)
                print(f"✓ Saved to {output_csv}")

        # Method 2: Using stream mode (for tables without clear borders)
        print("\n[Method 2] Stream mode (for borderless tables):")
        tables_stream = camelot.read_pdf(pdf_file, flavor='stream', pages='all')
        print(f"✓ Found {len(tables_stream)} table(s) with stream mode")

        for i, table in enumerate(tables_stream):
            print(f"\nStream Table {i+1}:")
            print(f"  - Shape: {table.df.shape}")
            print(f"  - Accuracy: {table.accuracy:.2f}%")
            print(f"\nStream Table {i+1} preview:")
            print(table.df.head(10))

            if i == 0:
                table.to_csv("output_camelot_stream.csv")

        # Export all tables
        if tables:
            tables.export(output_csv.replace('.csv', '_all.csv'), f='csv')

        elapsed_time = time.time() - start_time

        # Results summary
        print("\n" + "-"*80)
        print("RESULTS SUMMARY:")
        print(f"✓ Success: Yes")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Tables found (lattice): {len(tables)}")
        print(f"✓ Tables found (stream): {len(tables_stream)}")
        print(f"✓ Output file: {output_csv}")

        if tables:
            table = tables[0]
            completeness = (table.df.notna().sum().sum() / (table.df.shape[0] * table.df.shape[1]) * 100)
            print(f"✓ Data completeness: {completeness:.1f}%")
            print(f"✓ Rows extracted: {table.df.shape[0]}")
            print(f"✓ Columns extracted: {table.df.shape[1]}")
            print(f"✓ Extraction accuracy: {table.accuracy:.2f}%")

        return {
            'success': True,
            'quality_score': tables[0].accuracy if tables else 0,
            'time': elapsed_time,
            'tables_found': len(tables),
            'errors': None
        }

    except ImportError as e:
        print(f"\n✗ Camelot not properly installed: {str(e)}")
        print("Note: camelot-py requires ghostscript to be installed")
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
    result = test_camelot()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
