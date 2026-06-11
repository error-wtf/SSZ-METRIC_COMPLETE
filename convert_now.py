#!/usr/bin/env python3
import subprocess
import sys

# Install docling
subprocess.check_call([sys.executable, "-m", "pip", "install", "docling", "-q"])

from docling.document_converter import DocumentConverter
import os

converter = DocumentConverter()
output_dir = "/home/error/Downloads/ssz-metric-complete/pdfs_converted/"
os.makedirs(output_dir, exist_ok=True)

pdfs = [
    "/home/error/Downloads/SSZ-Framework Release Review.pdf",
    "/home/error/Downloads/Segmented Spacetime - Spiral Metric Й(r).pdf"
]

for pdf in pdfs:
    if os.path.exists(pdf):
        result = converter.convert(pdf)
        base = os.path.splitext(os.path.basename(pdf))[0]
        md_path = os.path.join(output_dir, f"{base}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(result.document.export_to_markdown())
        print(f"✅ Converted: {base}.md ({os.path.getsize(md_path)} bytes)")
    else:
        print(f"❌ Not found: {pdf}")
