import os
from fpdf import FPDF, XPos, YPos

class CYBReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            # Enhanced Header for First Page
            self.set_fill_color(31, 41, 55)
            self.rect(0, 0, 210, 35, 'F')
            self.set_y(12)
            self.set_font("helvetica", 'B', 18)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, "NETWORK DEFENSE & THREAT ANALYSIS", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.set_font("helvetica", '', 12)
            self.cell(0, 5, "Technical Audit Report | CYB-213 Academic Submission", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.ln(15)
        else:
            # Simpler header for subsequent pages
            self.set_fill_color(31, 41, 55)
            self.rect(0, 0, 210, 15, 'F')
            self.set_y(2)
            self.set_font("helvetica", 'B', 10)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, "CYB-213: Network Defense Audit", align='R')
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential Research Data", align='C')

    def chapter_title(self, title, level=1):
        self.set_text_color(20, 40, 80)
        if level == 1:
            self.ln(10)
            self.set_font("helvetica", 'B', 16)
            self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
            self.ln(5)
        elif level == 2:
            self.ln(6)
            self.set_font("helvetica", 'B', 14)
            self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)
        else:
            self.ln(4)
            self.set_font("helvetica", 'B', 12)
            self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_bullet(self, text):
        self.set_x(15)
        self.set_font("helvetica", '', 11)
        self.set_text_color(0, 0, 0)
        # Use ASCII bullet and multi_cell for wrapping
        self.multi_cell(0, 7, f"* {text.strip()}")
        self.ln(2)

    def add_paragraph(self, text):
        self.set_font("helvetica", '', 11)
        self.set_text_color(0, 0, 0)
        # Replace problematic Unicode characters
        text = text.replace('—', '-').replace('’', "'").replace('“', '"').replace('”', '"')
        self.multi_cell(0, 7, text)
        self.ln(2) # Reduced spacing

    def add_alert(self, text, type="NOTE"):
        self.set_fill_color(245, 245, 245)
        self.ln(1) # Reduced leading spacing
        if type == "WARNING":
            self.set_text_color(150, 0, 0)
        elif type == "CAUTION":
            self.set_text_color(200, 100, 0)
        else:
            self.set_text_color(0, 100, 150)
            
        self.set_font("helvetica", 'B', 10)
        self.cell(0, 8, f"[{type}]", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_font("helvetica", 'I', 10)
        self.multi_cell(0, 6, text.strip(), fill=True)
        self.ln(2) # Reduced trailing spacing
        self.set_text_color(0, 0, 0)

    def draw_table(self, header, data):
        self.ln(2)
        # Use fpdf2 built-in table component (v2.6+)
        with self.table(
            borders_layout="SINGLE_TOP_LINE",
            cell_fill_color=(245, 247, 250),
            cell_fill_mode="ROWS",
            line_height=6,
            text_align="LEFT",
            width=190,
        ) as table:
            # Header Row
            row = table.row()
            self.set_font("helvetica", 'B', 10)
            for h in header:
                row.cell(h)
            
            # Data Rows
            self.set_font("helvetica", '', 9)
            for d_row in data:
                row = table.row()
                for item in d_row:
                    clean_item = str(item).replace('**', '').replace('`', '').strip()
                    row.cell(clean_item)
        self.ln(2) # Reduced trailing spacing

def generate_premium_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = CYBReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    lines = content.split('\n')
    
    in_table = False
    table_header = []
    table_data = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
            
        if line.startswith('# '):
            pdf.chapter_title(line[2:], 1)
        elif line.startswith('## '):
            pdf.chapter_title(line[3:], 2)
        elif line.startswith('### '):
            pdf.chapter_title(line[4:], 3)
        elif line.startswith('- ') or line.startswith('* '):
            pdf.add_bullet(line[2:])
        elif line.startswith('> [!'):
            type_end = line.find(']')
            alert_type = line[4:type_end]
            alert_content = ""
            if i + 1 < len(lines) and lines[i+1].startswith('> '):
                 alert_content = lines[i+1][2:].strip()
            pdf.add_alert(alert_content, alert_type)
        elif line.startswith('|'):
            if '---' in line: continue
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if not in_table:
                in_table = True
                table_header = parts
            else:
                table_data.append(parts)
        elif line.startswith('!['):
            if in_table:
                pdf.draw_table(table_header, table_data)
                in_table = False
                table_data = []
            
            start = line.find('(') + 1
            end = line.find(')')
            img_path = line[start:end]
            if img_path.startswith('file://'):
                img_path = img_path[7:]
            
            if os.path.exists(img_path):
                # Check for space
                if pdf.get_y() > 180:
                    pdf.add_page()
                pdf.ln(2)
                pdf.image(img_path, w=140, x=35)
                # Caption
                if i + 1 < len(lines) and lines[i+1].startswith('*Figure'):
                    pdf.set_font("helvetica", 'I', 9)
                    pdf.set_text_color(100, 100, 100)
                    pdf.cell(0, 8, lines[i+1].strip('*'), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.set_text_color(0, 0, 0)
                pdf.ln(2)
        else:
            if in_table:
                pdf.draw_table(table_header, table_data)
                in_table = False
                table_data = []
            
            if not line.startswith('*Figure') and not line.startswith('---') and not line.startswith('> '):
                pdf.add_paragraph(line)

    if in_table:
        pdf.draw_table(table_header, table_data)

    pdf.output(pdf_path)

if __name__ == "__main__":
    generate_premium_pdf("results/defense_report.md", "results/defense_report.pdf")
