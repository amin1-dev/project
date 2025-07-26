from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse

def generate_career_report(user, recommendation):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(72, 720, f"Career Report for {user.username}")
    p.setFont("Helvetica", 12)
    p.drawString(72, 690, f"Top Career Recommendations:")
    careers = recommendation.top_careers.split(',')
    scores = recommendation.scores.split(',')
    for i, (career, score) in enumerate(zip(careers, scores)):
        p.drawString(100, 670 - i*20, f"{i+1}. Career: {career} | Confidence: {score}")
    p.drawString(72, 600, f"Generated on: {recommendation.generated_at.strftime('%Y-%m-%d %H:%M')}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"career_report_{user.username}.pdf")
