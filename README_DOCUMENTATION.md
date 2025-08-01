# FishCast AI - Dokumentasi Lengkap

## Cara Mengkonversi ke Word/PDF

Dokumentasi ini tersedia dalam format Markdown dan dapat dikonversi ke format Word (.docx) atau PDF. Berikut adalah beberapa cara untuk melakukan konversi:

### 1. Menggunakan Pandoc (Recommended)

#### Install Pandoc
```bash
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Windows
# Download dari https://pandoc.org/installing.html
```

#### Konversi ke Word
```bash
# Konversi semua bagian ke satu file Word
pandoc DOCUMENTATION_PART1.md DOCUMENTATION_PART2.md DOCUMENTATION_PART3.md \
  -o FishCast_AI_Documentation.docx \
  --toc \
  --number-sections \
  --reference-doc=template.docx
```

#### Konversi ke PDF
```bash
# Konversi ke PDF (memerlukan LaTeX)
pandoc DOCUMENTATION_PART1.md DOCUMENTATION_PART2.md DOCUMENTATION_PART3.md \
  -o FishCast_AI_Documentation.pdf \
  --toc \
  --number-sections \
  --pdf-engine=xelatex
```

### 2. Menggunakan Online Tools

#### Markdown to Word
1. Buka https://word.ai/ atau https://www.markdowntodocx.com/
2. Upload file Markdown
3. Download file Word

#### Markdown to PDF
1. Buka https://www.markdowntopdf.com/ atau https://md-to-pdf.fly.dev/
2. Upload file Markdown
3. Download file PDF

### 3. Menggunakan VS Code

#### Install Extensions
- "Markdown All in One"
- "Markdown PDF"
- "Pandoc Markdown Preview"

#### Convert to PDF
1. Buka file Markdown di VS Code
2. Press `Ctrl+Shift+P` (Windows/Linux) atau `Cmd+Shift+P` (macOS)
3. Type "Markdown PDF: Export (pdf)"
4. Select output location

### 4. Menggunakan Python Script

#### Install Dependencies
```bash
pip install markdown python-docx
```

#### Python Script untuk Konversi
```python
import markdown
from docx import Document
from docx.shared import Inches

def markdown_to_word(markdown_file, output_file):
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown.markdown(md_content, extensions=['toc', 'tables'])
    
    # Create Word document
    doc = Document()
    
    # Add title
    title = doc.add_heading('FishCast AI Documentation', 0)
    
    # Add content
    doc.add_paragraph(html_content)
    
    # Save document
    doc.save(output_file)

# Usage
markdown_to_word('DOCUMENTATION_PART1.md', 'FishCast_Documentation.docx')
```

### 5. Menggunakan LibreOffice

1. Buka LibreOffice Writer
2. File → Import → Markdown
3. Select file Markdown
4. File → Export → PDF

## Struktur Dokumentasi

Dokumentasi dibagi menjadi 3 bagian:

### Bagian 1: DOCUMENTATION_PART1.md
- Pendahuluan
- Arsitektur Sistem
- Struktur Database
- Alur Aplikasi

### Bagian 2: DOCUMENTATION_PART2.md
- Komponen Frontend
- API Endpoints
- Machine Learning Pipeline
- Cara Penggunaan

### Bagian 3: DOCUMENTATION_PART3.md
- Troubleshooting
- Pengembangan Selanjutnya
- Kesimpulan

## Format yang Didukung

### Input Formats
- Markdown (.md)
- HTML (.html)
- Text (.txt)

### Output Formats
- Microsoft Word (.docx)
- PDF (.pdf)
- HTML (.html)
- LaTeX (.tex)

## Tips untuk Hasil Terbaik

### 1. Styling
```bash
# Gunakan template Word untuk styling yang konsisten
pandoc input.md -o output.docx --reference-doc=template.docx
```

### 2. Table of Contents
```bash
# Tambahkan table of contents
pandoc input.md -o output.docx --toc --toc-depth=3
```

### 3. Numbered Sections
```bash
# Tambahkan nomor section
pandoc input.md -o output.docx --number-sections
```

### 4. Custom CSS (untuk HTML)
```bash
# Gunakan custom CSS untuk styling
pandoc input.md -o output.html --css=style.css
```

## Troubleshooting

### Pandoc Error
```bash
# Install LaTeX untuk PDF generation
sudo apt-get install texlive-full

# Atau gunakan wkhtmltopdf
sudo apt-get install wkhtmltopdf
```

### Font Issues
```bash
# Gunakan font yang support Unicode
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="DejaVu Sans"
```

### Image Issues
```bash
# Pastikan path gambar benar
pandoc input.md -o output.docx --extract-media=./media
```

## Contoh Command Lengkap

### Untuk Word dengan Styling
```bash
pandoc \
  DOCUMENTATION_PART1.md \
  DOCUMENTATION_PART2.md \
  DOCUMENTATION_PART3.md \
  -o FishCast_AI_Documentation.docx \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --reference-doc=template.docx \
  --metadata title="FishCast AI - Dokumentasi Lengkap" \
  --metadata author="FishCast AI Team" \
  --metadata date="$(date +%Y-%m-%d)"
```

### Untuk PDF dengan LaTeX
```bash
pandoc \
  DOCUMENTATION_PART1.md \
  DOCUMENTATION_PART2.md \
  DOCUMENTATION_PART3.md \
  -o FishCast_AI_Documentation.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  --metadata title="FishCast AI - Dokumentasi Lengkap" \
  --metadata author="FishCast AI Team" \
  --metadata date="$(date +%Y-%m-%d)"
```

## Metadata Template

Buat file `metadata.yaml`:
```yaml
---
title: "FishCast AI - Dokumentasi Lengkap"
author: "FishCast AI Team"
date: "2024-01-15"
version: "1.0.0"
django_version: "5.2.4"
status: "Development Complete - Ready for Production"
---

```

## Kontak Support

Jika mengalami masalah dengan konversi dokumentasi:
- **Email**: support@fishcast.ai
- **GitHub Issues**: https://github.com/fishcast-ai/issues
- **Documentation**: https://docs.fishcast.ai

---

*Dokumentasi ini dibuat pada: 2024-01-15*
*Versi: 1.0.0* 