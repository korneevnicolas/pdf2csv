"""
Generate a sample PDF file with a table for testing PDF to CSV conversion.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_sample_pdf(filename="sample_table.pdf"):
    """Create a sample PDF with a table."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Sample Sales Data", styles['Title'])
    elements.append(title)
    
    # Create table data
    data = [
        ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total'],
        ['Laptop', '15000', '18000', '17000', '20000', '70000'],
        ['Desktop', '8000', '7500', '8500', '9000', '33000'],
        ['Tablet', '12000', '13500', '14000', '15500', '55000'],
        ['Phone', '25000', '28000', '30000', '32000', '115000'],
        ['Monitor', '5000', '5500', '6000', '6500', '23000'],
    ]
    
    # Create table
    table = Table(data)
    
    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    print(f"Sample PDF created: {filename}")

if __name__ == "__main__":
    create_sample_pdf()
