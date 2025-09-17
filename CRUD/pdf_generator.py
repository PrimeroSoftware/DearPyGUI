# GENERADOR DE PDF PARA PERSONAS
# Contiene diferentes métodos para generar reportes PDF

import sqlite3
from datetime import datetime
import os

# Opción 1: Con ReportLab (más completa)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Opción 2: Con FPDF2 (más simple)
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

def get_personas_from_db(db_name="mydatabase.db"):
    """Obtiene todas las personas de la base de datos"""
    cnx = sqlite3.connect(db_name)
    c = cnx.cursor()
    c.execute("SELECT * FROM personas")
    personas = c.fetchall()
    cnx.close()
    return personas

def generate_pdf_reportlab(db_name="mydatabase.db"):
    """Genera PDF usando ReportLab (opción más completa)"""
    if not REPORTLAB_AVAILABLE:
        print("Error: ReportLab no está instalado. Instale con: pip install reportlab")
        return False
    
    try:
        personas = get_personas_from_db(db_name)
        
        if not personas:
            print("No hay personas en la base de datos para generar el reporte")
            return False
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_personas_reportlab_{timestamp}.pdf"
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Título del reporte
        title = Paragraph("REPORTE DE PERSONAS", title_style)
        elements.append(title)
        
        # Información del reporte
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=20
        )
        
        fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        info = Paragraph(f"Fecha de generación: {fecha_reporte}<br/>Total de registros: {len(personas)}", info_style)
        elements.append(info)
        
        # Crear tabla con los datos
        headers = ['ID', 'Nombre', 'Apellido', 'Edad']
        data = [headers]
        
        # Agregar datos de personas
        for persona in personas:
            data.append([str(persona[0]), persona[1], persona[2], str(persona[3])])
        
        # Crear la tabla
        table = Table(data, colWidths=[0.8*inch, 2*inch, 2*inch, 1*inch])
        
        # Estilo de la tabla
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Cuerpo de la tabla
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            
            # Alternar colores de filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
        ]))
        
        elements.append(table)
        
        # Agregar pie de página
        elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.gray,
            alignment=1  # Centrado
        )
        footer = Paragraph("Generado por Sistema CRUD de Personas - DearPyGUI", footer_style)
        elements.append(footer)
        
        # Construir el PDF
        doc.build(elements)
        
        print(f"PDF generado exitosamente: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al generar PDF con ReportLab: {str(e)}")
        return False

def generate_pdf_fpdf(db_name="mydatabase.db"):
    """Genera PDF usando FPDF2 (opción más simple)"""
    if not FPDF_AVAILABLE:
        print("Error: FPDF2 no está instalado. Instale con: pip install fpdf2")
        return False
    
    try:
        personas = get_personas_from_db(db_name)
        
        if not personas:
            print("No hay personas en la base de datos para generar el reporte")
            return False
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_personas_fpdf_{timestamp}.pdf"
        
        # Crear objeto PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 15, 'REPORTE DE PERSONAS', 0, 1, 'C')
        pdf.ln(5)
        
        # Información del reporte
        pdf.set_font('Arial', '', 10)
        fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pdf.cell(0, 8, f'Fecha de generación: {fecha_reporte}', 0, 1)
        pdf.cell(0, 8, f'Total de registros: {len(personas)}', 0, 1)
        pdf.ln(10)
        
        # Encabezados de la tabla
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(52, 73, 94)  # Color azul oscuro
        pdf.set_text_color(255, 255, 255)  # Texto blanco
        
        # Ancho de columnas
        col_widths = [25, 50, 50, 25]
        headers = ['ID', 'Nombre', 'Apellido', 'Edad']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos de la tabla
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)  # Texto negro
        
        for i, persona in enumerate(personas):
            # Alternar colores de fila
            if i % 2 == 0:
                pdf.set_fill_color(236, 240, 241)  # Gris claro
            else:
                pdf.set_fill_color(255, 255, 255)  # Blanco
            
            pdf.cell(col_widths[0], 8, str(persona[0]), 1, 0, 'C', True)
            pdf.cell(col_widths[1], 8, persona[1], 1, 0, 'L', True)
            pdf.cell(col_widths[2], 8, persona[2], 1, 0, 'L', True)
            pdf.cell(col_widths[3], 8, str(persona[3]), 1, 0, 'C', True)
            pdf.ln()
        
        # Pie de página
        pdf.ln(15)
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(128, 128, 128)  # Gris
        pdf.cell(0, 8, 'Generado por Sistema CRUD de Personas - DearPyGUI', 0, 1, 'C')
        
        # Guardar el archivo
        pdf.output(filename)
        
        print(f"PDF generado exitosamente: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al generar PDF con FPDF: {str(e)}")
        return False

def generate_simple_html_report(db_name="mydatabase.db"):
    """Genera un reporte HTML simple que se puede imprimir desde el navegador"""
    try:
        personas = get_personas_from_db(db_name)
        
        if not personas:
            print("No hay personas en la base de datos para generar el reporte")
            return False
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_personas_{timestamp}.txt"
        
        # Generar HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Personas</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .title {{
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .info {{
            color: #7f8c8d;
            font-size: 12px;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        td {{
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #e8f4fd;
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            font-size: 10px;
            margin-top: 30px;
        }}
        @media print {{
            body {{ margin: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">REPORTE DE PERSONAS</h1>
        <div class="info">
            Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}<br>
            Total de registros: {len(personas)}
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Edad</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Agregar datos de personas
        for persona in personas:
            html_content += f"""
            <tr>
                <td>{persona[0]}</td>
                <td>{persona[1]}</td>
                <td>{persona[2]}</td>
                <td>{persona[3]}</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
    
    <div class="footer">
        Generado por Sistema CRUD de Personas - DearPyGUI
    </div>
    
    <div class="no-print">
        <button onclick="window.print()" style="padding: 10px 20px; font-size: 16px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">
            Imprimir
        </button>
    </div>
</body>
</html>
"""
        
        # Guardar el archivo HTML
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Reporte HTML generado: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al generar reporte HTML: {str(e)}")
        return False

def open_file(filename):
    """Abre un archivo con la aplicación predeterminada del sistema"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(filename)
        elif os.name == 'posix':  # macOS y Linux
            os.system(f"xdg-open {filename}")
        return True
    except Exception as e:
        print(f"No se pudo abrir el archivo automáticamente: {e}")
        print(f"Archivo guardado como: {filename}")
        return False

# Funciones principales que se pueden llamar desde la interfaz
def print_personas_reportlab(db_name="mydatabase.db"):
    """Genera e intenta abrir PDF con ReportLab"""
    filename = generate_pdf_reportlab(db_name)
    if filename:
        open_file(filename)
        return True
    return False

def print_personas_fpdf(db_name="mydatabase.db"):
    """Genera e intenta abrir PDF con FPDF"""
    filename = generate_pdf_fpdf(db_name)
    if filename:
        open_file(filename)
        return True
    return False

def print_personas_html(db_name="mydatabase.db"):
    """Genera e intenta abrir reporte HTML"""
    filename = generate_simple_html_report(db_name)
    if filename:
        open_file(filename)
        return True
    return False

if __name__ == "__main__":
    # Prueba las diferentes opciones
    print("Probando generación de reportes...")
    
    # Probar ReportLab
    if REPORTLAB_AVAILABLE:
        print("1. Generando PDF con ReportLab...")
        print_personas_reportlab()
    else:
        print("1. ReportLab no disponible")
    
    # Probar FPDF
    if FPDF_AVAILABLE:
        print("2. Generando PDF con FPDF...")
        print_personas_fpdf()
    else:
        print("2. FPDF no disponible")
    
    # Probar HTML
    # print("3. Generando reporte HTML...")
    # print_personas_html()
