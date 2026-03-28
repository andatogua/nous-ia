from datetime import datetime
from fpdf import FPDF
import unicodedata
import matplotlib.pyplot as plt
import tempfile
from services.statistics_service import StatisticsService
from services.report_service import ReportService
from services.profile_service import ProfileService
from services.activity_service import ActivityService
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
    def write_line(pdf, text, font_style="", font_size=10, line_height=5):
        pdf.set_font("Helvetica", font_style, font_size)
        pdf.set_x(10)
        pdf.multi_cell(190, line_height, PDFReportService.clean_text(text))

    @staticmethod
    def write_cell_line(pdf, text, width=95, font_style="", font_size=10, align="L"):
        pdf.set_font("Helvetica", font_style, font_size)
        pdf.cell(width, 5, PDFReportService.clean_text(text), 0, 0, align)

    @staticmethod
    def section_title(pdf, text):
        pdf.ln(1.5)
        pdf.set_fill_color(230, 240, 255)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(10)
        pdf.cell(190, 7, PDFReportService.clean_text(text), ln=True, fill=True)
        pdf.ln(0.5)

    @staticmethod
    def draw_progress_bar(pdf, label, value, max_value, suffix="", bar_color=(74, 144, 226)):
        if max_value <= 0:
            max_value = 1

        percentage = max(0, min(value / max_value, 1))

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_x(10)
        pdf.cell(190, 5, PDFReportService.clean_text(f"{label}: {value}{suffix}"), ln=True)

        x = 10
        y = pdf.get_y()
        width = 190
        height = 4

        pdf.set_fill_color(232, 232, 232)
        pdf.rect(x, y, width, height, style="F")

        pdf.set_fill_color(*bar_color)
        pdf.rect(x, y, width * percentage, height, style="F")

        pdf.ln(6)

    @staticmethod
    def truncate_text(text, max_length=150):
        text = PDFReportService.clean_text(text)
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."

    @staticmethod
    def generate_general_interpretation(last_phq9, last_who5):
        if not last_phq9 and not last_who5:
            return "No existen suficientes datos para elaborar una interpretacion general del estado actual."

        messages = []

        if last_phq9:
            messages.append(
                f"El ultimo resultado PHQ-9 fue {last_phq9['PUNTAJE_TOTAL']} puntos con nivel {last_phq9['NIVEL_RESULTADO']}."
            )

        if last_who5:
            messages.append(
                f"El ultimo resultado WHO-5 fue {last_who5['PUNTAJE_ESCALADO']} puntos con nivel {last_who5['NIVEL_RESULTADO']}."
            )

        if last_phq9 and last_who5:
            phq_score = last_phq9["PUNTAJE_TOTAL"]
            who_score = float(last_who5["PUNTAJE_ESCALADO"])

            if phq_score >= 10 or who_score < 52:
                messages.append(
                    "Se recomienda mantener seguimiento del bienestar emocional y aplicar las actividades sugeridas por el sistema."
                )
            else:
                messages.append(
                    "No se observa una alerta elevada en este momento, aunque se recomienda continuar con habitos de autocuidado."
                )

        return " ".join(messages)

    @staticmethod
    def get_status_label(last_phq9, last_who5):
        if not last_phq9 and not last_who5:
            return "SIN DATOS"

        phq_score = last_phq9["PUNTAJE_TOTAL"] if last_phq9 else 0
        who_score = float(last_who5["PUNTAJE_ESCALADO"]) if last_who5 else 100

        if phq_score >= 15 or who_score < 40:
            return "RIESGO ALTO"
        elif phq_score >= 10 or who_score < 52:
            return "RIESGO MODERADO"
        else:
            return "ESTABLE"

    @staticmethod
    def get_phq_bar_color(score):
        if score <= 4:
            return (46, 160, 67)
        elif score <= 9:
            return (255, 193, 7)
        elif score <= 14:
            return (255, 152, 0)
        else:
            return (220, 53, 69)

    @staticmethod
    def get_who_bar_color(score):
        if score >= 80:
            return (46, 160, 67)
        elif score >= 52:
            return (255, 152, 0)
        else:
            return (220, 53, 69)
    
    @staticmethod
    def generate_evolution_chart(data):
        fechas_phq = []
        valores_phq = []

        fechas_who = []
        valores_who = []

        for row in data:
            fecha = row["FECHA_FIN"]

            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%d/%m/%Y")

            if row["CODIGO"] == "PHQ-9":
                fechas_phq.append(fecha)
                valores_phq.append(row["PUNTAJE_TOTAL"])

            elif row["CODIGO"] == "WHO-5":
                fechas_who.append(fecha)
                valores_who.append(row["PUNTAJE_ESCALADO"])

        if not fechas_phq and not fechas_who:
            return None

        plt.figure(figsize=(8, 4.2))

        if fechas_phq:
            plt.plot(fechas_phq, valores_phq, marker="o", label="PHQ-9")

        if fechas_who:
            plt.plot(fechas_who, valores_who, marker="o", label="WHO-5")

        plt.xlabel("Fecha de evaluación")
        plt.ylabel("Puntaje")
        plt.title("Evolución de resultados")
        plt.legend()
        plt.tight_layout()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_file.name, dpi=120, bbox_inches="tight")
        plt.close()

        return temp_file.name

    @staticmethod
    def generate_pdf_report(user_id, output_path="reporte_usuario.pdf"):
        profile = ProfileService.get_profile(user_id)
        summary = ReportService.get_progress_summary(user_id)
        recommendations = RecommendationRepository.get_latest_recommendations_by_user(user_id, limit=3)
        activity_progress = ActivityService.get_activity_progress_summary(user_id)

        if not profile:
            return False, "No se pudo obtener el perfil del usuario.", None

        pdf = FPDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_top_margin(8)
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()

        last_phq9 = summary.get("last_phq9")
        last_who5 = summary.get("last_who5")
        

        # =========================
        # ENCABEZADO
        # =========================

        # Logo solo icono, centrado y más pequeño
        try:
            pdf.image("assets/logo_nousia_icon.png", x=88, y=8, w=34)
            pdf.ln(32)
        except:
            pdf.ln(8)

        pdf.set_text_color(35, 35, 35)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(190, 6, "Reporte ejecutivo del usuario", ln=True, align="C")

        pdf.set_font("Helvetica", "", 9)
        pdf.cell(190, 5, "Sistema de apoyo para la salud mental", ln=True, align="C")

        pdf.ln(2)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        PDFReportService.write_line(
            pdf,
            f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            9,
            4.5
        )

        # =========================
        # SEMAFORO DE BIENESTAR
        # =========================
        PDFReportService.section_title(pdf, "Estado actual del usuario")

        status = PDFReportService.get_status_label(last_phq9, last_who5)
        PDFReportService.write_line(pdf, f"Semaforo de bienestar: {status}", "B", 10, 5)

        # =========================
        # DATOS DEL USUARIO
        # =========================
        PDFReportService.section_title(pdf, "Datos del usuario")

        pdf.set_font("Helvetica", "", 9)
        pdf.set_x(10)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Nombre: {profile['NOMBRE']} {profile['APELLIDO']}"), 0, 0)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Cedula: {profile['CEDULA']}"), 0, 1)

        pdf.set_x(10)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Correo: {profile['CORREO']}"), 0, 0)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Usuario: {profile['USERNAME']}"), 0, 1)

        pdf.set_x(10)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Fecha de nacimiento: {profile['FECHA_NACIMIENTO']}"), 0, 0)
        pdf.cell(95, 5, PDFReportService.clean_text(f"Sexo: {profile['SEXO']}"), 0, 1)

        # =========================
        # RESULTADOS DE EVALUACION
        # =========================
        PDFReportService.section_title(pdf, "Resultados principales")

        if last_phq9:
            phq_score = int(last_phq9["PUNTAJE_TOTAL"])
            PDFReportService.write_line(
                pdf,
                f"PHQ-9 | Nivel: {last_phq9['NIVEL_RESULTADO']}",
                "B",
                9,
                4.5
            )
            PDFReportService.draw_progress_bar(
                pdf,
                "Puntaje PHQ-9",
                phq_score,
                27,
                bar_color=PDFReportService.get_phq_bar_color(phq_score)
            )
        else:
            PDFReportService.write_line(pdf, "No hay resultado reciente de PHQ-9.", "", 9, 4.5)

        if last_who5:
            who_score = float(last_who5["PUNTAJE_ESCALADO"])
            PDFReportService.write_line(
                pdf,
                f"WHO-5 | Nivel: {last_who5['NIVEL_RESULTADO']}",
                "B",
                9,
                4.5
            )
            PDFReportService.draw_progress_bar(
                pdf,
                "Puntaje WHO-5",
                who_score,
                100,
                bar_color=PDFReportService.get_who_bar_color(who_score)
            )
        else:
            PDFReportService.write_line(pdf, "No hay resultado reciente de WHO-5.", "", 9, 4.5)

        # =========================
        # GRAFICA DE EVOLUCION
        # =========================

        statistics = StatisticsService.get_user_statistics(user_id)
        chart_path = PDFReportService.generate_evolution_chart(statistics["data"])

        if chart_path:
            chart_width = 170
            chart_height = 90

            if pdf.get_y() + chart_height > 270:
                pdf.add_page()

            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(190, 6, "Evolucion de resultados", ln=True)

            pdf.ln(2)
            x_center = (210 - chart_width) / 2
            pdf.image(chart_path, x=x_center, y=pdf.get_y(), w=chart_width, h=chart_height)
            pdf.ln(chart_height + 4)

        # =========================
        # INTERPRETACION GENERAL
        # =========================
        PDFReportService.section_title(pdf, "Interpretacion general")

        general_text = PDFReportService.generate_general_interpretation(last_phq9, last_who5)
        general_text = PDFReportService.truncate_text(general_text, 260)
        PDFReportService.write_line(pdf, general_text, "", 9, 4.5)

        # =========================
        # CUMPLIMIENTO DE ACTIVIDADES
        # =========================
        PDFReportService.section_title(pdf, "Cumplimiento de actividades")

        if activity_progress["total"] > 0:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_x(10)
            pdf.cell(63, 5, PDFReportService.clean_text(f"Total: {activity_progress['total']}"), 0, 0)
            pdf.cell(63, 5, PDFReportService.clean_text(f"Realizadas: {activity_progress['realizadas']}"), 0, 0)
            pdf.cell(64, 5, PDFReportService.clean_text(f"No realizadas: {activity_progress['no_realizadas']}"), 0, 1)

            PDFReportService.draw_progress_bar(
                pdf,
                "Cumplimiento",
                float(activity_progress["porcentaje_cumplimiento"]),
                100,
                suffix="%",
                bar_color=(46, 160, 67)
            )
        else:
            PDFReportService.write_line(
                pdf,
                "Todavia no existen actividades de seguimiento registradas para este usuario.",
                "",
                9,
                4.5
            )

        # =========================
        # RECOMENDACIONES CLAVE
        # =========================
        PDFReportService.section_title(pdf, "Recomendaciones clave")

        if recommendations:
            for i, rec in enumerate(recommendations, start=1):
                titulo = PDFReportService.clean_text(rec.get("TITULO", "Recomendacion"))
                descripcion = PDFReportService.clean_text(rec.get("DESCRIPCION", ""))

                titulo = PDFReportService.truncate_text(titulo, 60)
                descripcion = PDFReportService.truncate_text(descripcion, 155)

                PDFReportService.write_line(pdf, f"{i}. {titulo}", "B", 9, 4.5)
                PDFReportService.write_line(pdf, descripcion, "", 8.5, 4.2)
                pdf.ln(0.3)
        else:
            PDFReportService.write_line(
                pdf,
                "No hay recomendaciones registradas en la base de datos.",
                "",
                9,
                4.5
            )

        # =========================
        # AVISO PROFESIONAL
        # =========================
        PDFReportService.section_title(pdf, "Aviso importante")

        aviso = (
            "Este reporte tiene fines educativos y orientativos. "
            "No constituye un diagnostico clinico ni reemplaza la atencion profesional."
        )
        PDFReportService.write_line(pdf, aviso, "", 8.5, 4.2)

        pdf.ln(1)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

        pdf.set_font("Helvetica", "I", 8.5)
        pdf.cell(
            190,
            4,
            "Reporte generado automaticamente por el Sistema Web de Apoyo Educativo",
            ln=True,
            align="C"
        )

        pdf.output(output_path)
        return True, "Reporte PDF generado correctamente.", output_path