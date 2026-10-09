"""Convert the generated lesson-plan PDF to an editable DOCX."""
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from pdf2docx import Converter

from pdf.generator import generate_lesson_plan_pdf


def generate_lesson_plan_docx(buffer, data):
    """Convert the PDF export so Word output follows the same page layout."""
    pdf_buffer = BytesIO()
    generate_lesson_plan_pdf(pdf_buffer, data)

    with TemporaryDirectory(prefix="lesson-plan-docx-") as temp_dir:
        pdf_path = Path(temp_dir) / "lesson-plan.pdf"
        docx_path = Path(temp_dir) / "lesson-plan.docx"
        pdf_path.write_bytes(pdf_buffer.getvalue())

        converter = Converter(str(pdf_path))
        try:
            converter.convert(str(docx_path), multi_processing=False)
        finally:
            converter.close()

        buffer.write(docx_path.read_bytes())
