from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import os.path
from pathlib import Path

def get_basic_info():
    """Get the basic information about the switchboard."""
    sales_order = input("Please enter the Sales Order Number: ")
    customer = input("Please enter the Customer name: ")
    job_info = input("Please enter the Job Name or Address: ")
    switchboard = input("Please enter the switchboard name: ")
    return sales_order, customer, job_info, switchboard

def get_number_of_sections():
    """Get and validate the number of sections."""
    while True:
        try:
            sections = int(input("How many sections? (Enter a whole number): "))
            if sections > 0:
                return sections
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid whole number.")

def get_common_dimensions():
    """Get common height and depth if all sections share the same dimensions."""
    common_dimensions = input("Do all sections have the same height and depth? (yes/no): ").lower().strip()
    common_dimensions = common_dimensions in ['yes', 'y']
    
    if not common_dimensions:
        return None, None, False
        
    while True:
        try:
            common_height = float(input("Enter the common Height: "))
            common_depth = float(input("Enter the common Depth: "))
            return common_height, common_depth, True
        except ValueError:
            print("Please enter valid numbers for height and depth")

def check_l_sections():
    """Check if the switchboard has any L sections."""
    has_l_sections = input("Does this switchboard have any L sections? (yes/no): ").lower().strip()
    return has_l_sections in ['yes', 'y']

def get_section_dimensions(section_num, common_height=None, common_depth=None, has_common_dimensions=False, is_l_section=False):
    """Get dimensions for a single section."""
    while True:
        try:
            if is_l_section:
                width = float(input(f"Enter Corner Width for Section {section_num}: "))
            else:
                width = float(input(f"Enter Width for Section {section_num}: "))
            
            if not has_common_dimensions:
                height = float(input(f"Enter Height for Section {section_num}: "))
                if is_l_section:
                    depth = float(input(f"Enter Corner Depth for Section {section_num}: "))
                else:
                    depth = float(input(f"Enter Depth for Section {section_num}: "))
            else:
                height = common_height
                depth = common_depth
            
            return width, height, depth
        except ValueError:
            print("Please enter valid numbers for dimensions")

def get_section_type(has_l_sections):
    """Get the section type (S or L) if applicable."""
    if not has_l_sections:
        return 'S'
        
    while True:
        section_type = input("Enter type (S or L): ").upper()
        if section_type in ['S', 'L']:
            return section_type
        print("Please enter either S or L for type")

def calculate_parts(section_info):
    """Calculate the number of parts for a section."""
    # Each section has 4 pieces for each dimension
    width_pieces = 4
    height_pieces = 4
    depth_pieces = 4
    
    # For L sections, we need additional pieces for the corner
    if section_info['type'] == 'L':
        corner_pieces = 4
    else:
        corner_pieces = 0
    
    total_pieces = width_pieces + height_pieces + depth_pieces + corner_pieces
    
    return {
        'width_pieces': width_pieces,
        'height_pieces': height_pieces,
        'depth_pieces': depth_pieces,
        'corner_pieces': corner_pieces,
        'total_pieces': total_pieces
    }

def process_sections(num_sections, common_height, common_depth, has_common_dimensions, has_l_sections):
    """Process all sections and collect their information."""
    sections = []
    for i in range(num_sections):
        print(f"\nSection {i + 1}:")
        section_type = get_section_type(has_l_sections)
        width, height, depth = get_section_dimensions(i + 1, common_height, common_depth, has_common_dimensions, section_type == 'L')
        
        section_info = {
            'width': width,
            'height': height,
            'depth': depth,
            'type': section_type
        }
        
        # Calculate parts for this section
        parts = calculate_parts(section_info)
        section_info['parts'] = parts
        
        sections.append(section_info)
    
    return sections

def check_another_switchboard():
    """Check if user wants to enter another switchboard."""
    while True:
        response = input("\nIs there another switchboard? (yes/no): ").lower().strip()
        if response in ['yes', 'y', 'no', 'n']:
            return response in ['yes', 'y']
        print("Please enter 'yes' or 'no'")

def process_switchboard():
    """Process a single switchboard and return its information."""
    # Get basic information
    sales_order, customer, job_info, switchboard = get_basic_info()
    
    # Get number of sections
    num_sections = get_number_of_sections()
    
    # Get common dimensions if applicable (skip if only 1 section)
    common_height = None
    common_depth = None
    has_common_dimensions = False
    if num_sections > 1:
        common_height, common_depth, has_common_dimensions = get_common_dimensions()
    
    # Check for L sections (skip if 2 or fewer sections)
    has_l_sections = False
    if num_sections > 2:
        has_l_sections = check_l_sections()
    
    # Process all sections
    sections = process_sections(num_sections, common_height, common_depth, has_common_dimensions, has_l_sections)
    
    return {
        'sales_order': sales_order,
        'customer': customer,
        'job_info': job_info,
        'switchboard': switchboard,
        'sections': sections
    }

def get_report_name():
    """Get report name from user and check for file conflicts."""
    # Change this to save in the output directory instead of /app
    current_dir = "./output"
    
    # Create output directory if it doesn't exist
    os.makedirs(current_dir, exist_ok=True)
    
    while True:
        report_name = input("\nEnter a name for the report (without .pdf): ").strip()
        if not report_name:
            print("Report name cannot be empty. Please try again.")
            continue
            
        filename = os.path.join(current_dir, f"{report_name} - Parts Report.pdf")
        if os.path.exists(filename):
            while True:
                response = input(f"File '{filename}' already exists. Overwrite? (yes/no): ").lower().strip()
                if response in ['yes', 'y']:
                    return report_name, filename
                elif response in ['no', 'n']:
                    break
                print("Please enter 'yes' or 'no'")
        else:
            return report_name, filename

def generate_parts_report(all_switchboards):
    """Generate a PDF report of all parts needed."""
    # Get report name and filename from user
    report_name, filename = get_report_name()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        filename, 
        pagesize=letter, 
        leftMargin=50, 
        rightMargin=50, 
        topMargin=50, 
        bottomMargin=50
    )
    styles = getSampleStyleSheet()
    elements = []
    
    # Define styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=20
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey
    )
    
    # Add title to first page
    elements.append(Paragraph(f"{report_name} - Parts Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Track unique dimensions and their piece counts
    width_pieces = {'S': {}, 'L': {}}
    height_pieces = {'S': {}, 'L': {}}
    depth_pieces = {'S': {}, 'L': {}}
    
    for switchboard in all_switchboards:
        # Add switchboard header
        elements.append(Paragraph(f"Switchboard: {switchboard['switchboard']}", styles['Heading2']))
        elements.append(Paragraph(f"Sales Order: {switchboard['sales_order']}", styles['Normal']))
        elements.append(Paragraph(f"Customer: {switchboard['customer']}", styles['Normal']))
        elements.append(Paragraph(f"Job Info: {switchboard['job_info']}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Create section data
        section_data = [['Section', 'Type', 'Width (qty)', 'Height (qty)', 'Depth (qty)', 'Corner']]
        
        for i, section in enumerate(switchboard['sections'], 1):
            parts = section['parts']
            section_type = section['type']
            
            # Format dimensions to show decimals only when not zero
            width_str = f"{section['width']:.2f}".rstrip('0').rstrip('.')
            height_str = f"{section['height']:.2f}".rstrip('0').rstrip('.')
            depth_str = f"{section['depth']:.2f}".rstrip('0').rstrip('.')
            
            # Track pieces for each dimension
            width_key = f"{width_str}\""
            height_key = f"{height_str}\""
            depth_key = f"{depth_str}\""
            
            if width_key not in width_pieces[section_type]:
                width_pieces[section_type][width_key] = 0
            if height_key not in height_pieces[section_type]:
                height_pieces[section_type][height_key] = 0
            if depth_key not in depth_pieces[section_type]:
                depth_pieces[section_type][depth_key] = 0
                
            width_pieces[section_type][width_key] += parts['width_pieces']
            height_pieces[section_type][height_key] += parts['height_pieces']
            depth_pieces[section_type][depth_key] += parts['depth_pieces']
            
            section_data.append([
                f"Section {i}",
                section['type'],
                f"{width_str}\" ({parts['width_pieces']})",
                f"{height_str}\" ({parts['height_pieces']})",
                f"{depth_str}\" ({parts['depth_pieces']})",
                "Yes" if section['type'] == 'L' else "No"
            ])
        
        # Create and style the table
        table = Table(section_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Add page break before dimension totals
    elements.append(PageBreak())
    
    # Add title to new page
    elements.append(Paragraph(f"{report_name} - Parts Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Add dimension totals
    elements.append(Paragraph("Dimension Totals", styles['Heading2']))
    
    # Width totals
    elements.append(Paragraph("Width Pieces", styles['Heading3']))
    width_data = [['Width', 'Standard Pieces', 'Corner Pieces']]
    
    # Get all unique widths
    all_widths = sorted(set(list(width_pieces['S'].keys()) + list(width_pieces['L'].keys())))
    
    for width in all_widths:
        width_data.append([
            width,
            str(width_pieces['S'].get(width, 0)),
            str(width_pieces['L'].get(width, 0))
        ])
    
    width_table = Table(width_data)
    width_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(width_table)
    elements.append(Spacer(1, 12))
    
    # Height totals
    elements.append(Paragraph("Height Pieces", styles['Heading3']))
    height_data = [['Height', 'Standard Pieces', 'Corner Pieces']]
    
    # Get all unique heights
    all_heights = sorted(set(list(height_pieces['S'].keys()) + list(height_pieces['L'].keys())))
    
    for height in all_heights:
        height_data.append([
            height,
            str(height_pieces['S'].get(height, 0)),
            str(height_pieces['L'].get(height, 0))
        ])
    
    height_table = Table(height_data)
    height_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(height_table)
    elements.append(Spacer(1, 12))
    
    # Depth totals
    elements.append(Paragraph("Depth Pieces", styles['Heading3']))
    depth_data = [['Depth', 'Standard Pieces', 'Corner Pieces']]
    
    # Get all unique depths
    all_depths = sorted(set(list(depth_pieces['S'].keys()) + list(depth_pieces['L'].keys())))
    
    for depth in all_depths:
        depth_data.append([
            depth,
            str(depth_pieces['S'].get(depth, 0)),
            str(depth_pieces['L'].get(depth, 0))
        ])
    
    depth_table = Table(depth_data)
    depth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(depth_table)
    
    # Build the PDF
    doc.build(elements)
    print(f"\nReport generated: {filename}")

def main():
    all_switchboards = []
    
    while True:
        # Process current switchboard
        switchboard_info = process_switchboard()
        all_switchboards.append(switchboard_info)
        
        # Check if there's another switchboard
        if not check_another_switchboard():
            break
    
    # Generate the PDF report
    generate_parts_report(all_switchboards)

if __name__ == "__main__":
    main() 