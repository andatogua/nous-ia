from datetime import datetime
from fpdf import FPDF
import unicodedata

from services.report_service import ReportService
from services.profile_service import ProfileService
from repositories.recommendation_repository import RecommendationRepository


class PDFReportService:

    @staticmethod
    def clean_text(text):
        if text is None:
            return ""

        text = str(text)
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
        text = text.replace("\r", " ").replace("\n", " ")
        text = " ".join(text.split())
        return text

    @staticmethod
    def write_line(pdf, text, font_style="", font_size=11):
        pdf.set_font("Helvetica", font_style, font_size)
        pdf.set_x(10)
        pdf.multi_cell(190, 7, PDFReportService.clean_text(text))

    @staticmethod
    def generate_pdf_report(user_id, output_path="reporte_usuario.pdf"):
        profile = ProfileService.get_profile(user_id)
        summary = ReportService.get_progress_summary(user_id)
        recommendations = RecommendationRepository.get_latest_recommendations_by_user(user_id, limit=3)

        if not profile:
            return False, "No se pudo obtener el perfil del usuario.", None

        pdf = FPDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Título
        PDFReportService.write_line(pdf, "Reporte de progreso del usuario", "B", 16)
        PDFReportService.write_line(
            pdf,
            f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            11
        )
        pdf.ln(3)

        # Datos del usuario
        PDFReportService.write_line(pdf, "Datos del usuario", "B", 13)
        PDFReportService.write_line(pdf, f"Nombre: {profile['NOMBRE']} {profile['APELLIDO']}")
        PDFReportService.write_line(pdf, f"Cedula: {profile['CEDULA']}")
        PDFReportService.write_line(pdf, f"Correo: {profile['CORREO']}")
        PDFReportService.write_line(pdf, f"Usuario: {profile['USERNAME']}")
        pdf.ln(3)

        # Resumen del progreso
        PDFReportService.write_line(pdf, "Resumen del progreso", "B", 13)

        last_phq9 = summary.get("last_phq9")
        last_who5 = summary.get("last_who5")
        latest_mood = summary.get("latest_mood")

        if last_phq9:
            PDFReportService.write_line(
                pdf,
                f"Ultimo PHQ-9: {last_phq9['PUNTAJE_TOTAL']} | Nivel: {last_phq9['NIVEL_RESULTADO']}"
            )
            PDFReportService.write_line(
                pdf,
                f"Interpretacion PHQ-9: {last_phq9['INTERPRETACION']}"
            )

        if last_who5:
            PDFReportService.write_line(
                pdf,
                f"Ultimo WHO-5: {last_who5['PUNTAJE_ESCALADO']} | Nivel: {last_who5['NIVEL_RESULTADO']}"
            )
            PDFReportService.write_line(
                pdf,
                f"Interpretacion WHO-5: {last_who5['INTERPRETACION']}"
            )

        pdf.ln(3)

        # Estado emocional
        PDFReportService.write_line(pdf, "Ultimo estado emocional", "B", 13)

        if latest_mood:
            PDFReportService.write_line(pdf, f"Emocion: {latest_mood['NOMBRE_EMOCION']}")
            PDFReportService.write_line(pdf, f"Intensidad: {latest_mood['NIVEL_INTENSIDAD']} / 5")
            PDFReportService.write_line(
                pdf,
                f"Observacion: {latest_mood['OBSERVACION'] if latest_mood['OBSERVACION'] else 'Sin observacion.'}"
            )
        else:
            PDFReportService.write_line(pdf, "No hay registros emocionales recientes.")

        pdf.ln(3)

        # Recomendaciones
        PDFReportService.write_line(pdf, "Recomendaciones recientes", "B", 13)

        if recommendations:
            for i, rec in enumerate(recommendations, start=1):
                PDFReportService.write_line(
                    pdf,
                    f"{i}. {rec.get('TITULO', 'Recomendacion')}",
                    "B",
                    11
                )
                PDFReportService.write_line(
                    pdf,
                    rec.get("DESCRIPCION", "")
                )
                pdf.ln(2)
        else:
            PDFReportService.write_line(pdf, "No hay recomendaciones registradas en la base de datos.")

        pdf.output(output_path)
        return True, "Reporte PDF generado correctamente.", output_path