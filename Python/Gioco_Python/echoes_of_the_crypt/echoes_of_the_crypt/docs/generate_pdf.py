#!/usr/bin/env python3
"""Genera PDF dalla documentazione tecnica markdown."""
from fpdf import FPDF
import markdown
import re
import os

class TechDocPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=20)
        # Font con supporto Unicode
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf', uni=True)
        self.add_font('DejaVu', 'BI', '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf', uni=True)
        self.add_font('DejaVuMono', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', uni=True)

    def header(self):
        if self.page_no() > 1:
            self.set_font('DejaVu', 'I', 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, 'Echoes of the Crypt - Documentazione Tecnica', align='C')
            self.ln(8)
            self.set_draw_color(180, 180, 180)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def section_title(self, num, title):
        self.set_font('DejaVu', 'B', 14)
        self.set_text_color(40, 40, 80)
        self.cell(0, 10, f'{num}) {title}', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(40, 40, 80)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def subsection_title(self, title):
        self.set_font('DejaVu', 'B', 11)
        self.set_text_color(60, 60, 100)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('DejaVu', '', 9.5)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin)
        self.multi_cell(self.w - self.l_margin - self.r_margin, 5, text)
        self.ln(2)
        self.set_x(self.l_margin)

    def code_block(self, code):
        self.set_font('DejaVuMono', '', 7.5)
        self.set_fill_color(240, 240, 245)
        self.set_draw_color(200, 200, 210)
        # Calcola altezza
        lines = code.split('\n')
        x = self.l_margin
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        line_h = 4
        h = len(lines) * line_h + 4
        # Controlla page break
        if y + h > self.h - 20:
            self.add_page()
            y = self.get_y()
            x = self.l_margin
        self.rect(x, y, w, h, style='DF')
        self.set_xy(x + 2, y + 2)
        for line in lines:
            self.cell(w - 4, line_h, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_x(self.l_margin)

    def table_row(self, cells, widths, header=False, fill=False):
        style = 'B' if header else ''
        self.set_font('DejaVu', style, 8)
        if header:
            self.set_fill_color(60, 60, 100)
            self.set_text_color(255, 255, 255)
        elif fill:
            self.set_fill_color(245, 245, 250)
            self.set_text_color(30, 30, 30)
        else:
            self.set_text_color(30, 30, 30)

        max_h = 5
        self.set_x(self.l_margin)
        for i, (cell, w) in enumerate(zip(cells, widths)):
            self.cell(w, max_h, str(cell)[:int(w/1.8)], border=1, fill=fill or header)
        self.ln(max_h)
        self.set_x(self.l_margin)


def parse_markdown_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = TechDocPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title page
    pdf.ln(30)
    pdf.set_font('DejaVu', 'B', 28)
    pdf.set_text_color(40, 40, 80)
    pdf.cell(0, 15, 'Echoes of the Crypt', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('DejaVu', '', 16)
    pdf.set_text_color(80, 80, 120)
    pdf.cell(0, 10, 'Documentazione Tecnica', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, 'Progetto d\'esame ITS Cloud Specialist', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'Studente: Luca Tarallo', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'Data: 27/11/2026', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'Repository: ohTara/Materie_ITS', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('DejaVu', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, 'Dungeon crawler roguelike in Python/pygame-ce con generazione procedurale,\nsistema progressione personaggi, SQLite persistence, build cross-platform.', align='C')

    # Parse sections
    lines = content.split('\n')
    i = 0
    section_num = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Code block detection
        if line.startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                pdf.code_block('\n'.join(code_lines))
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            # Main title - skip (already on title page)
            pass
        elif line.startswith('## '):
            section_num += 1
            pdf.add_page()
            pdf.section_title(chr(96 + section_num), line[3:].strip())
        elif line.startswith('### '):
            pdf.subsection_title(line[4:].strip())
        elif line.startswith('#### '):
            pdf.set_font('DejaVu', 'BI', 10)
            pdf.set_text_color(80, 80, 100)
            pdf.cell(0, 6, line[5:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        # Tables
        elif '|' in line and i + 1 < len(lines) and '|' in lines[i + 1] and '---' in lines[i + 1]:
            # Parse table
            header_cells = [c.strip() for c in line.split('|')[1:-1]]
            sep_line = lines[i + 1]
            data_lines = []
            j = i + 2
            while j < len(lines) and '|' in lines[j]:
                data_lines.append([c.strip() for c in lines[j].split('|')[1:-1]])
                j += 1

            # Calculate column widths
            col_count = len(header_cells)
            total_w = pdf.w - pdf.l_margin - pdf.r_margin
            col_w = total_w / col_count

            pdf.table_row(header_cells, [col_w]*col_count, header=True)
            for idx, row in enumerate(data_lines):
                pdf.table_row(row, [col_w]*col_count, fill=(idx % 2 == 0))
            pdf.ln(3)
            i = j
            continue
        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            pdf.set_font('DejaVu', '', 9.5)
            pdf.set_text_color(30, 30, 30)
            bullet_text = line.strip()[2:]
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5, f'• {bullet_text}')
            pdf.set_x(pdf.l_margin)
        # Numbered list
        elif re.match(r'^\d+\.\s', line.strip()):
            pdf.set_font('DejaVu', '', 9.5)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5, line.strip())
            pdf.set_x(pdf.l_margin)
        # Bold/italic inline - simplified
        elif line.strip() and not line.startswith('---'):
            # Clean markdown formatting
            clean = line
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
            clean = re.sub(r'\*(.+?)\*', r'\1', clean)
            clean = re.sub(r'`(.+?)`', r'\1', clean)
            clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean)
            if clean.strip():
                pdf.body_text(clean.strip())

        i += 1

    pdf.output(pdf_path)
    print(f"PDF generato: {pdf_path} ({pdf.page_no()} pagine)")


if __name__ == '__main__':
    md_file = os.path.join(os.path.dirname(__file__), 'technical_documentation.md')
    pdf_file = os.path.join(os.path.dirname(__file__), 'Documentazione_Tecnica_Echoes_of_the_Crypt.pdf')
    parse_markdown_to_pdf(md_file, pdf_file)