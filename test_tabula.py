"""
Test tabula-py library for PDF to CSV conversion
"""
import tabula
import time
import pandas as pd

def test_tabula():
    """Test tabula-py library"""
    print("\n" + "="*80)
    print("TESTING: tabula-py")
    print("="*80)

    pdf_file = "sample_table.pdf"
    output_csv = "output_tabula.csv"

    try:
        start_time = time.time()

        # Method 1: Direct conversion to CSV
        print("\n[Method 1] Direct PDF to CSV conversion:")
        tabula.convert_into(pdf_file, output_csv, output_format="csv", pages='all')
        print(f"✓ Successfully created {output_csv}")

        # Read and display the output
        with open(output_csv, 'r') as f:
            content = f.read()
            print("\nExtracted CSV content:")
            print(content[:500])  # First 500 chars

        # Method 2: Read as DataFrame
        print("\n[Method 2] Read as pandas DataFrame:")
        dfs = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        print(f"✓ Found {len(dfs)} table(s)")

        for i, df in enumerate(dfs):
            print(f"\nTable {i+1} shape: {df.shape}")
            print(f"Table {i+1} preview:")
            print(df.head(10))

            # Save each table
            if len(dfs) > 1:
                df.to_csv(f"output_tabula_table_{i+1}.csv", index=False)

        # Method 3: With lattice mode (for tables with clear borders)
        print("\n[Method 3] Using lattice mode (for bordered tables):")
        dfs_lattice = tabula.read_pdf(pdf_file, pages='all', lattice=True, multiple_tables=True)
        print(f"✓ Found {len(dfs_lattice)} table(s) with lattice mode")

        for i, df in enumerate(dfs_lattice):
            print(f"\nLattice Table {i+1} shape: {df.shape}")
            print(f"Lattice Table {i+1} preview:")
            print(df.head(10))

        elapsed_time = time.time() - start_time

        # Results summary
        print("\n" + "-"*80)
        print("RESULTS SUMMARY:")
        print(f"✓ Success: Yes")
        print(f"✓ Time taken: {elapsed_time:.2f} seconds")
        print(f"✓ Number of tables found: {len(dfs)}")
        print(f"✓ Output file: {output_csv}")

        # Quality assessment
        if dfs:
            df = dfs[0]
            completeness = (df.notna().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
            print(f"✓ Data completeness: {completeness:.1f}%")
            print(f"✓ Rows extracted: {df.shape[0]}")
            print(f"✓ Columns extracted: {df.shape[1]}")

        return {
            'success': True,
            'quality_score': 0,  # To be manually assessed
            'time': elapsed_time,
            'tables_found': len(dfs),
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
    result = test_tabula()
    print("\n" + "="*80)
    print(f"Test Result: {'PASSED' if result['success'] else 'FAILED'}")
    print("="*80)
