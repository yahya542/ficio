#!/usr/bin/env python3
"""
FishCast AI Documentation Converter
Script untuk mengkonversi dokumentasi Markdown ke Word dan PDF
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        print("✓ Pandoc is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Pandoc is not installed. Please install it first:")
        print("  Ubuntu/Debian: sudo apt-get install pandoc")
        print("  macOS: brew install pandoc")
        print("  Windows: Download from https://pandoc.org/installing.html")
        return False
    
    return True

def create_metadata_file():
    """Create metadata file for pandoc"""
    metadata_content = f"""---
title: "FishCast AI - Dokumentasi Lengkap"
author: "FishCast AI Team"
date: "{datetime.now().strftime('%Y-%m-%d')}"
version: "1.0.0"
django_version: "5.2.4"
status: "Development Complete - Ready for Production"
---
"""
    
    with open('metadata.yaml', 'w', encoding='utf-8') as f:
        f.write(metadata_content)
    
    print("✓ Created metadata.yaml")

def convert_to_word():
    """Convert documentation to Word format"""
    print("\n🔄 Converting to Word format...")
    
    cmd = [
        'pandoc',
        'DOCUMENTATION_PART1.md',
        'DOCUMENTATION_PART2.md', 
        'DOCUMENTATION_PART3.md',
        '-o', 'FishCast_AI_Documentation.docx',
        '--toc',
        '--toc-depth=3',
        '--number-sections',
        '--metadata-file=metadata.yaml',
        '--reference-doc=template.docx' if os.path.exists('template.docx') else None
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✓ Successfully created FishCast_AI_Documentation.docx")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting to Word: {e}")
        print(f"Error output: {e.stderr}")
        return False

def convert_to_pdf():
    """Convert documentation to PDF format"""
    print("\n🔄 Converting to PDF format...")
    
    cmd = [
        'pandoc',
        'DOCUMENTATION_PART1.md',
        'DOCUMENTATION_PART2.md',
        'DOCUMENTATION_PART3.md',
        '-o', 'FishCast_AI_Documentation.pdf',
        '--toc',
        '--toc-depth=3',
        '--number-sections',
        '--pdf-engine=xelatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=11pt',
        '-V', 'mainfont=DejaVu Sans',
        '-V', 'monofont=DejaVu Sans Mono',
        '--metadata-file=metadata.yaml'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✓ Successfully created FishCast_AI_Documentation.pdf")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting to PDF: {e}")
        print(f"Error output: {e.stderr}")
        print("\n💡 Try installing LaTeX:")
        print("  Ubuntu/Debian: sudo apt-get install texlive-full")
        print("  macOS: brew install basictex")
        return False

def convert_to_html():
    """Convert documentation to HTML format"""
    print("\n🔄 Converting to HTML format...")
    
    cmd = [
        'pandoc',
        'DOCUMENTATION_PART1.md',
        'DOCUMENTATION_PART2.md',
        'DOCUMENTATION_PART3.md',
        '-o', 'FishCast_AI_Documentation.html',
        '--toc',
        '--toc-depth=3',
        '--number-sections',
        '--metadata-file=metadata.yaml',
        '--standalone',
        '--css=style.css' if os.path.exists('style.css') else None
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✓ Successfully created FishCast_AI_Documentation.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting to HTML: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_css_template():
    """Create a basic CSS template for HTML styling"""
    css_content = """/* FishCast AI Documentation Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

.document {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

h2 {
    color: #34495e;
    margin-top: 30px;
}

h3 {
    color: #7f8c8d;
}

code {
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
}

pre {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #3498db;
    color: white;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}

.toc {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 30px;
}

.toc h2 {
    margin-top: 0;
}

.toc ul {
    list-style-type: none;
    padding-left: 0;
}

.toc li {
    margin: 5px 0;
}

.toc a {
    text-decoration: none;
    color: #3498db;
}

.toc a:hover {
    text-decoration: underline;
}
"""
    
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✓ Created style.css template")

def check_files():
    """Check if all required documentation files exist"""
    required_files = [
        'DOCUMENTATION_PART1.md',
        'DOCUMENTATION_PART2.md', 
        'DOCUMENTATION_PART3.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing required files: {', '.join(missing_files)}")
        print("Please make sure all documentation files are present in the current directory.")
        return False
    
    print("✓ All required documentation files found")
    return True

def main():
    parser = argparse.ArgumentParser(description='Convert FishCast AI documentation to various formats')
    parser.add_argument('--format', choices=['word', 'pdf', 'html', 'all'], 
                       default='all', help='Output format (default: all)')
    parser.add_argument('--create-css', action='store_true', 
                       help='Create CSS template for HTML styling')
    
    args = parser.parse_args()
    
    print("🐟 FishCast AI Documentation Converter")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check required files
    if not check_files():
        sys.exit(1)
    
    # Create metadata file
    create_metadata_file()
    
    # Create CSS template if requested
    if args.create_css:
        create_css_template()
    
    success_count = 0
    total_count = 0
    
    # Convert based on format
    if args.format in ['word', 'all']:
        total_count += 1
        if convert_to_word():
            success_count += 1
    
    if args.format in ['pdf', 'all']:
        total_count += 1
        if convert_to_pdf():
            success_count += 1
    
    if args.format in ['html', 'all']:
        total_count += 1
        if convert_to_html():
            success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Conversion Summary: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("🎉 All conversions completed successfully!")
        print("\n📁 Generated files:")
        if os.path.exists('FishCast_AI_Documentation.docx'):
            print("  • FishCast_AI_Documentation.docx")
        if os.path.exists('FishCast_AI_Documentation.pdf'):
            print("  • FishCast_AI_Documentation.pdf")
        if os.path.exists('FishCast_AI_Documentation.html'):
            print("  • FishCast_AI_Documentation.html")
    else:
        print("⚠️  Some conversions failed. Check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 