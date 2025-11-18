#!/usr/bin/env python3
"""
PDF to CSV Converter - Production Ready Solution
Uses pdfplumber for optimal speed and accuracy

Usage:
    python pdf2csv.py input.pdf [output.csv]
    python pdf2csv.py input.pdf --all-tables
"""

import pdfplumber
import csv
import sys
import argparse
from pathlib import Path
from typing import List, Optional, Tuple


def extract_tables_from_pdf(
    pdf_path: str,
    pages: Optional[List[int]] = None,
    table_settings: Optional[dict] = None
) -> Tuple[List[List[List[str]]], dict]:
    """
    Extract all tables from a PDF file

    Args:
        pdf_path: Path to the PDF file
        pages: List of page numbers to process (0-indexed), None for all pages
        table_settings: Custom table extraction settings

    Returns:
        Tuple of (list of tables, metadata dict)
        Each table is a list of rows, each row is a list of cell values
    """
    # Default table settings optimized for most PDFs
    if table_settings is None:
        table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_tolerance": 3,
        }

    all_tables = []
    metadata = {
        'total_pages': 0,
        'pages_processed': 0,
        'tables_found': 0,
        'total_rows': 0,
    }

    with pdfplumber.open(pdf_path) as pdf:
        metadata['total_pages'] = len(pdf.pages)

        # Determine which pages to process
        if pages is None:
            pages_to_process = pdf.pages
        else:
            pages_to_process = [pdf.pages[i] for i in pages if i < len(pdf.pages)]

        metadata['pages_processed'] = len(pages_to_process)

        # Extract tables from each page
        for page_num, page in enumerate(pages_to_process, 1):
            tables = page.extract_tables(table_settings=table_settings)

            for table in tables:
                if table:  # Skip empty tables
                    all_tables.append(table)
                    metadata['tables_found'] += 1
                    metadata['total_rows'] += len(table)

    return all_tables, metadata


def save_tables_to_csv(
    tables: List[List[List[str]]],
    output_path: str,
    combine_tables: bool = True,
    skip_duplicate_headers: bool = True
) -> None:
    """
    Save extracted tables to CSV file(s)

    Args:
        tables: List of tables (each table is a list of rows)
        output_path: Output CSV file path
        combine_tables: If True, combine all tables into one CSV, else save separately
        skip_duplicate_headers: If True and combining tables, skip headers after the first
    """
    output_path = Path(output_path)

    if not tables:
        print("⚠ No tables found to save")
        return

    if combine_tables:
        # Combine all tables into one CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            for table_num, table in enumerate(tables):
                if table_num == 0:
                    # Write all rows including header for first table
                    writer.writerows(table)
                else:
                    # Skip header row for subsequent tables if requested
                    start_row = 1 if skip_duplicate_headers else 0
                    writer.writerows(table[start_row:])

        print(f"✓ Combined {len(tables)} table(s) into {output_path}")

    else:
        # Save each table separately
        for i, table in enumerate(tables):
            if len(tables) > 1:
                # Add table number to filename
                table_output = output_path.parent / f"{output_path.stem}_table_{i+1}{output_path.suffix}"
            else:
                table_output = output_path

            with open(table_output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(table)

            print(f"✓ Saved table {i+1} to {table_output}")


def pdf_to_csv(
    pdf_path: str,
    csv_path: Optional[str] = None,
    all_tables: bool = False,
    pages: Optional[List[int]] = None,
    verbose: bool = True
) -> dict:
    """
    Main function to convert PDF tables to CSV

    Args:
        pdf_path: Path to input PDF file
        csv_path: Path to output CSV file (default: same name as PDF with .csv)
        all_tables: If True, save each table separately
        pages: List of page numbers to process (default: all)
        verbose: Print progress information

    Returns:
        Dictionary with conversion metadata
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Determine output path
    if csv_path is None:
        csv_path = pdf_path.with_suffix('.csv')
    else:
        csv_path = Path(csv_path)

    if verbose:
        print(f"Converting: {pdf_path}")
        print(f"Output: {csv_path}")
        print("-" * 60)

    # Extract tables
    tables, metadata = extract_tables_from_pdf(pdf_path, pages=pages)

    if verbose:
        print(f"✓ Processed {metadata['pages_processed']}/{metadata['total_pages']} page(s)")
        print(f"✓ Found {metadata['tables_found']} table(s)")
        print(f"✓ Total rows: {metadata['total_rows']}")
        print("-" * 60)

    # Save to CSV
    if tables:
        save_tables_to_csv(
            tables,
            csv_path,
            combine_tables=not all_tables,
            skip_duplicate_headers=True
        )

        if verbose:
            print("✓ Conversion completed successfully!")
    else:
        if verbose:
            print("⚠ No tables found in PDF")

    return metadata


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Convert PDF tables to CSV using pdfplumber',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                    # Convert to input.csv
  %(prog)s input.pdf output.csv         # Specify output file
  %(prog)s input.pdf --all-tables       # Save each table separately
  %(prog)s input.pdf --pages 0 2 4      # Process only pages 1, 3, and 5
        """
    )

    parser.add_argument('pdf_file', help='Input PDF file')
    parser.add_argument('csv_file', nargs='?', help='Output CSV file (optional)')
    parser.add_argument('--all-tables', action='store_true',
                        help='Save each table to a separate CSV file')
    parser.add_argument('--pages', type=int, nargs='+',
                        help='Page numbers to process (0-indexed)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress output messages')

    args = parser.parse_args()

    try:
        metadata = pdf_to_csv(
            pdf_path=args.pdf_file,
            csv_path=args.csv_file,
            all_tables=args.all_tables,
            pages=args.pages,
            verbose=not args.quiet
        )

        # Exit with success
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
