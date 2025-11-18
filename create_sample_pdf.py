"""
Create a sample PDF with a table for testing PDF to CSV conversion libraries.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_sample_pdf():
    """Create a PDF with a sample table"""
    pdf_file = "sample_table.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Container for elements
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Sales Report - Q4 2023", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Sample table data
    data = [
        ['Product ID', 'Product Name', 'Category', 'Quantity Sold', 'Unit Price', 'Total Revenue'],
        ['P001', 'Laptop Pro 15', 'Electronics', '145', '$1,299.99', '$188,498.55'],
        ['P002', 'Wireless Mouse', 'Accessories', '432', '$29.99', '$12,955.68'],
        ['P003', 'USB-C Cable', 'Accessories', '789', '$12.99', '$10,249.11'],
        ['P004', 'Monitor 27"', 'Electronics', '267', '$399.99', '$106,797.33'],
        ['P005', 'Keyboard Mechanical', 'Accessories', '198', '$89.99', '$17,818.02'],
        ['P006', 'Webcam HD', 'Electronics', '356', '$79.99', '$28,476.44'],
        ['P007', 'Desk Lamp LED', 'Office', '423', '$45.99', '$19,453.77'],
        ['P008', 'Office Chair', 'Furniture', '89', '$249.99', '$22,249.11'],
        ['P009', 'Standing Desk', 'Furniture', '67', '$599.99', '$40,199.33'],
        ['P010', 'Headphones Wireless', 'Electronics', '512', '$149.99', '$76,794.88'],
        ['', '', '', 'TOTAL:', '', '$523,492.22']
    ]

    # Create table
    table = Table(data)

    # Add style to table
    table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Data rows styling
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (3, 1), (5, -1), 'RIGHT'),  # Right align numbers

        # Total row styling
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)
    print(f"Created sample PDF: {pdf_file}")
    return pdf_file

if __name__ == "__main__":
    create_sample_pdf()
