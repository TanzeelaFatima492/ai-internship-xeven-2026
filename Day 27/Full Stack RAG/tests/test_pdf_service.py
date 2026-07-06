from app.services.pdf_service import PDFService

text = PDFService.extract_text(
    "data/uploads/sample.pdf"
)

print(text)