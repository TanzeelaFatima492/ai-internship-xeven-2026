from app.services.pdf_service import PDFService

service = PDFService()

text = service.extract_text(
    "data/sample.pdf"
)

print(text)