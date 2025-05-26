from pathlib import Path
from docling.document_converter import DocumentConverter

def pdf_to_md(pdf_path:Path, md_path:Path = Path('output') / 'md.md'):
    try:
        converter = DocumentConverter()

        result_md = converter.convert(pdf_path)

        with open(md_path, "x", encoding="utf-8") as file:
            file.write(result_md.document.export_to_markdown())

    except Exception as e:
        return e