#!/usr/bin/env python3
"""Convert PDFs to Markdown using docling."""

import os
from docling.document_converter import DocumentConverter

def convert_pdf(pdf_path, output_dir):
    """Convert a single PDF to Markdown."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, f"{base_name}.md")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(result.document.export_to_markdown())
    
    print(f"✅ Converted: {base_name}.pdf -> {base_name}.md")
    print(f"   Size: {os.path.getsize(md_path)} bytes")
    return md_path

if __name__ == "__main__":
    output_dir = "/home/error/Downloads/ssz-metric-complete/pdfs_converted/"
    os.makedirs(output_dir, exist_ok=True)
    
    pdfs = [
        "/home/error/Downloads/SSZ-Framework Release Review.pdf",
        "/home/error/Downloads/Segmented Spacetime - Spiral Metric Й(r).pdf"
    ]
    
    for pdf in pdfs:
        if os.path.exists(pdf):
            convert_pdf(pdf, output_dir)
        else:
            print(f"❌ PDF not found: {pdf}")
