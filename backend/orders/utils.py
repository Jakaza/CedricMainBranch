import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.conf import settings
from datetime import datetime
import requests
from PIL import Image as PILImage


def generate_receipt_pdf(order):
    """
    Generate a PDF receipt for an order with plan details and images
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
    )
    
    # Generate receipt number if not exists
    receipt_number = order.generate_receipt_number()
    
    # Header - Company Name
    company_name = Paragraph(
        f"<b>Cedric House Planning</b>",
        title_style
    )
    elements.append(company_name)
    
    # Receipt Title
    receipt_title = Paragraph("<b>PAYMENT RECEIPT</b>", heading_style)
    elements.append(receipt_title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Receipt Details Table
    receipt_info_data = [
        ['Receipt Number:', receipt_number],
        ['Order ID:', f"#{order.id}"],
        ['Date:', order.created_at.strftime('%B %d, %Y %I:%M %p')],
        ['Payment Status:', order.status],
    ]
    
    if order.customer_email:
        receipt_info_data.insert(3, ['Customer Email:', order.customer_email])
    
    receipt_info_table = Table(receipt_info_data, colWidths=[2*inch, 4*inch])
    receipt_info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(receipt_info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Plan Details Section
    plan_heading = Paragraph("<b>HOUSE PLAN DETAILS</b>", heading_style)
    elements.append(plan_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    # Try to add plan image if available
    if order.plan.images and len(order.plan.images.all()) > 0:
        try:
            # Get first image
            first_image = order.plan.images.all()[0]
            image_url = first_image.image.url
            
            # Download and add image
            if image_url.startswith('http'):
                response = requests.get(image_url, timeout=5)
                img_buffer = io.BytesIO(response.content)
            else:
                # Local file
                img_buffer = first_image.image.path
            
            img = Image(img_buffer, width=4*inch, height=3*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.2*inch))
        except Exception as e:
            print(f"Could not add image to PDF: {e}")
            # Continue without image
    
    # Plan Information Table
    plan_data = [
        ['Plan Name:', order.plan.title],
        ['Category:', order.plan.get_category_display()],
        ['Bedrooms:', str(order.plan.bedrooms)],
        ['Bathrooms:', str(order.plan.bathrooms)],
        ['Garage:', str(order.plan.garage)],
        ['Floor Area:', f"{order.plan.floor_area} m²"],
        ['Levels:', str(order.plan.levels)],
        ['Dimensions:', f"{order.plan.width}m × {order.plan.depth}m"],
    ]
    
    if order.plan.styles:
        styles_str = ', '.join(order.plan.styles[:3])  # Show first 3 styles
        plan_data.append(['Style:', styles_str])
    
    plan_table = Table(plan_data, colWidths=[2*inch, 4*inch])
    plan_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#dedede')),
    ]))
    elements.append(plan_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Summary
    payment_heading = Paragraph("<b>PAYMENT SUMMARY</b>", heading_style)
    elements.append(payment_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    payment_data = [
        ['Item', 'Amount'],
        [order.plan.title, f"R {order.amount:,.2f}"],
        ['', ''],
        ['TOTAL PAID', f"R {order.amount:,.2f}"],
    ]
    
    payment_table = Table(payment_data, colWidths=[4*inch, 2*inch])
    payment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#dedede')),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#4caf50')),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = Paragraph(
        "<i>Thank you for your purchase! This receipt serves as proof of payment.</i>",
        ParagraphStyle(
            'Footer',
            parent=normal_style,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#888888'),
            fontSize=9
        )
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    
    # Mark receipt as generated
    order.receipt_generated = True
    order.save()
    
    # Get the PDF value
    buffer.seek(0)
    return buffer
