import re
import streamlit as st
from ui.styles import load_styles
from ui.sidebar import render_sidebar
from utils.session_manager import initialize_session, logout

st.set_page_config(
    page_title="Sistema principal",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
initialize_session()

if not st.session_state.user:
    st.switch_page("pages/login.py")

user = st.session_state.user
full_name = f"{user['NOMBRE']} {user['APELLIDO']}"

def clean_recommendation_text(text):
    if not text:
        return ""

    text = str(text)

    # Quitar fences de código
    text = text.replace("```html", "")
    text = text.replace("```json", "")
    text = text.replace("```markdown", "")
    text = text.replace("```", "")

    # Eliminar etiquetas HTML
    text = re.sub(r"<[^>]+>", "", text)

    # Reemplazar entidades comunes
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")

    # Limpiar espacios extras
    text = re.sub(r"\s+", " ", text).strip()

    return text
# ==================================
# ESTADO DEL FLUJO DE EVALUACIONES
# ==================================
if "evaluation_step" not in st.session_state:
    st.session_state.evaluation_step = "intro"

if "phq9_score" not in st.session_state:
    st.session_state.phq9_score = None

if "who5_score" not in st.session_state:
    st.session_state.who5_score = None

if "recommendations_generated" not in st.session_state:
    st.session_state.recommendations_generated = False

if "recommendations_data" not in st.session_state:
    st.session_state.recommendations_data = []

selected = render_sidebar(full_name)

# ==================================
# DATOS INFORMATIVOS
# ==================================
if selected == "Datos informativos":
    st.markdown("""
    <div class="content-header">
        <div class="content-badge">Módulo informativo</div>
        <h1>Datos informativos</h1>
        <p>
            En esta sección encontrará información básica sobre el sistema, la depresión,
            los cuestionarios utilizados y la finalidad educativa del proyecto.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ¿Qué es este sistema?")
    st.write("""
    Este sistema web de apoyo educativo ha sido diseñado para orientar al usuario en la detección inicial
    y autogestión de síntomas relacionados con la depresión. Permite realizar cuestionarios, registrar
    estados emocionales, visualizar estadísticas y recibir recomendaciones de apoyo.
    """)

    st.markdown("## Objetivo del sistema")
    st.write("""
    El objetivo principal es brindar una herramienta digital de orientación que ayude al usuario a conocer
    mejor su estado emocional, identificar señales de alerta y fomentar el autocuidado, siempre desde un
    enfoque educativo y no sustitutivo de la atención profesional.
    """)

    st.markdown("## ¿Qué es la depresión?")
    st.write("""
    La depresión es un trastorno del estado de ánimo que puede afectar la forma en que una persona piensa,
    siente y actúa. Puede manifestarse mediante tristeza persistente, pérdida de interés, fatiga, cambios
    en el sueño, dificultades para concentrarse y sensación de desesperanza.
    """)

    st.markdown("## Síntomas frecuentes")
    st.markdown("""
    - Tristeza constante o sensación de vacío  
    - Pérdida de interés en actividades cotidianas  
    - Cansancio o falta de energía  
    - Alteraciones del sueño  
    - Cambios en el apetito  
    - Dificultad para concentrarse  
    - Baja autoestima o culpa excesiva  
    - Pensamientos negativos persistentes
    """)

    st.markdown("## Sobre los cuestionarios")
    st.markdown("""
    **PHQ-9**  
    Evalúa síntomas relacionados con depresión.

    **WHO-5**  
    Evalúa bienestar psicológico general.
    """)

    st.info("""
    Este sistema no reemplaza a un psicólogo ni psiquiatra.
    Los resultados son orientativos.
    """)

# ==================================
# ESTADÍSTICAS
# ==================================
elif selected == "Estadísticas":

    from services.statistics_service import StatisticsService
    import pandas as pd
    import plotly.express as px

    st.title("Estadísticas del usuario")

    stats = StatisticsService.get_user_statistics(user["ID_USUARIO"])

    if stats["total"] == 0:

        st.info("Todavía no hay evaluaciones para mostrar estadísticas.")

    else:

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric("Evaluaciones totales", stats["total"])

        with col2:
            st.metric("Promedio PHQ-9", stats["avg_phq"])

        with col3:
            st.metric("Promedio WHO-5", stats["avg_who"])

        df = pd.DataFrame(stats["data"])

        df["FECHA_FIN"] = pd.to_datetime(df["FECHA_FIN"])

        st.divider()

        st.subheader("Evolución de resultados")

        fig = px.line(
            df,
            x="FECHA_FIN",
            y="PUNTAJE_TOTAL",
            color="CODIGO",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("Distribución de niveles")

        fig2 = px.histogram(
            df,
            x="NIVEL_RESULTADO",
            color="CODIGO"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ==================================
# EVALUACIONES
# ==================================
elif selected == "Evaluaciones":
    from services.evaluation_service import EvaluationService

    st.title("Evaluaciones")

    if st.session_state.evaluation_step == "intro":
        st.subheader("Bienvenido al módulo de evaluación")

        st.write("Aquí podrá realizar dos cuestionarios:")

        st.markdown("""
        - **PHQ-9**: orientado a identificar síntomas depresivos.  
        - **WHO-5**: orientado a evaluar bienestar emocional.
        """)

        st.warning("""
        Responda con sinceridad. Esta evaluación es de apoyo educativo y no sustituye atención profesional.
        """)

        if st.button("Comenzar evaluación", use_container_width=True):
            st.session_state.evaluation_step = "phq9"
            st.rerun()

    elif st.session_state.evaluation_step == "phq9":
        st.subheader("Cuestionario PHQ-9")

        questionnaire, questions, options = EvaluationService.get_questionnaire_data("PHQ-9")

        if not questionnaire or not questions or not options:
            st.error("No se pudo cargar el cuestionario PHQ-9 desde la base de datos.")
        else:
            option_map = {
                option["ID_OPCION"]: {
                    "texto": option["TEXTO_OPCION"],
                    "valor": option["VALOR"]
                }
                for option in options
            }

            with st.form("form_phq9"):
                selected_answers = []

                for question in questions:
                    selected_option_id = st.radio(
                        f"{question['ORDEN_PREGUNTA']}. {question['TEXTO_PREGUNTA']}",
                        options=list(option_map.keys()),
                        format_func=lambda x: option_map[x]["texto"],
                        key=f"phq9_{question['ID_PREGUNTA']}"
                    )

                    selected_answers.append({
                        "id_pregunta": question["ID_PREGUNTA"],
                        "id_opcion": selected_option_id,
                        "valor": option_map[selected_option_id]["valor"]
                    })

                enviar_phq9 = st.form_submit_button("Siguiente: WHO-5", use_container_width=True)

            if enviar_phq9:
                ok, message, result_data = EvaluationService.save_single_evaluation(
                    user["ID_USUARIO"],
                    "PHQ-9",
                    selected_answers
                )

                if ok:
                    st.session_state.phq9_score = result_data["puntaje_total"]
                    st.session_state.evaluation_step = "who5"
                    st.success("PHQ-9 guardado correctamente.")
                    st.rerun()
                else:
                    st.error(message)

    elif st.session_state.evaluation_step == "who5":
        st.subheader("Cuestionario WHO-5")

        questionnaire, questions, options = EvaluationService.get_questionnaire_data("WHO-5")

        if not questionnaire or not questions or not options:
            st.error("No se pudo cargar el cuestionario WHO-5 desde la base de datos.")
        else:
            option_map = {
                option["ID_OPCION"]: {
                    "texto": option["TEXTO_OPCION"],
                    "valor": option["VALOR"]
                }
                for option in options
            }

            with st.form("form_who5"):
                selected_answers = []

                for question in questions:
                    selected_option_id = st.radio(
                        f"{question['ORDEN_PREGUNTA']}. {question['TEXTO_PREGUNTA']}",
                        options=list(option_map.keys()),
                        format_func=lambda x: option_map[x]["texto"],
                        key=f"who5_{question['ID_PREGUNTA']}"
                    )

                    selected_answers.append({
                        "id_pregunta": question["ID_PREGUNTA"],
                        "id_opcion": selected_option_id,
                        "valor": option_map[selected_option_id]["valor"]
                    })

                enviar_who5 = st.form_submit_button("Finalizar evaluación", use_container_width=True)

            if enviar_who5:
                ok, message, result_data = EvaluationService.save_single_evaluation(
                    user["ID_USUARIO"],
                    "WHO-5",
                    selected_answers
                )

                if ok:
                    st.session_state.who5_score = result_data["puntaje_total"]
                    st.session_state.evaluation_step = "results"
                    st.success("WHO-5 guardado correctamente.")
                    st.rerun()
                else:
                    st.error(message)

    elif st.session_state.evaluation_step == "results":
        st.title("Resultados de la evaluación")

        phq9 = st.session_state.phq9_score
        who5 = st.session_state.who5_score
        who5_escalado = who5 * 4 if who5 is not None else 0

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Resultado PHQ-9")
            st.metric("Puntaje obtenido", phq9 if phq9 is not None else 0)
            st.progress((phq9 if phq9 is not None else 0) / 27)

            if phq9 is not None:
                if phq9 <= 4:
                    st.success("Nivel: Mínima")
                    st.write("Presencia mínima de síntomas depresivos.")
                elif phq9 <= 9:
                    st.info("Nivel: Leve")
                    st.write("Presencia leve de síntomas depresivos.")
                elif phq9 <= 14:
                    st.warning("Nivel: Moderada")
                    st.write("Presencia moderada de síntomas depresivos.")
                elif phq9 <= 19:
                    st.warning("Nivel: Moderadamente severa")
                    st.write("Presencia importante de síntomas depresivos.")
                else:
                    st.error("Nivel: Severa")
                    st.write("Presencia severa de síntomas depresivos. Se recomienda atención profesional.")

        with col2:
            st.subheader("Resultado WHO-5")
            st.metric("Puntaje obtenido", who5_escalado)
            st.progress(who5_escalado / 100)

            if who5_escalado >= 80:
                st.success("Nivel: Bienestar alto")
                st.write("El usuario presenta un nivel alto de bienestar emocional.")
            elif who5_escalado >= 52:
                st.info("Nivel: Bienestar medio")
                st.write("El usuario presenta un nivel intermedio de bienestar emocional.")
            else:
                st.warning("Nivel: Bienestar bajo")
                st.write("El usuario presenta bajo bienestar emocional. Se recomienda seguimiento.")

        st.divider()
        st.subheader("Interpretación general")

        if phq9 is not None and (phq9 >= 10 or who5_escalado < 52):
            st.warning("""
            Los resultados sugieren que sería conveniente dar seguimiento al estado emocional del usuario
            y considerar orientación profesional si los síntomas persisten.
            """)
        else:
            st.success("""
            Los resultados no reflejan señales elevadas en este momento, pero se recomienda mantener seguimiento
            y hábitos de autocuidado.
            """)

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Realizar nuevamente", use_container_width=True):
                st.session_state.evaluation_step = "intro"
                st.session_state.phq9_score = None
                st.session_state.who5_score = None
                st.rerun()

        with col_b:
            if st.button("Ir a historial", use_container_width=True):
                st.info("En el siguiente paso conectaremos esta sección al historial real.")

# ==================================
# HISTORIAL
# ==================================
elif selected == "Historial":
    from services.history_service import HistoryService
    import pandas as pd

    st.title("Historial de evaluaciones")
    st.write("Aquí podrá consultar las evaluaciones realizadas y sus resultados.")

    history = HistoryService.get_user_history(user["ID_USUARIO"])

    if not history:
        st.info("Todavía no hay evaluaciones registradas.")
    else:
        df = pd.DataFrame(history)

        df["FECHA_FIN"] = pd.to_datetime(df["FECHA_FIN"]).dt.strftime("%Y-%m-%d %H:%M")

        st.dataframe(
            df[[
                "FECHA_FIN",
                "CUESTIONARIO",
                "PUNTAJE_TOTAL",
                "PUNTAJE_ESCALADO",
                "NIVEL_RESULTADO",
                "INTERPRETACION"
            ]],
            use_container_width=True
        )

        st.markdown("## Detalle de resultados")

        for item in history:
            with st.expander(f"{item['CUESTIONARIO']} - {item['FECHA_FIN']}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Cuestionario:** {item['CUESTIONARIO']}")
                    st.write(f"**Puntaje total:** {item['PUNTAJE_TOTAL']}")
                    st.write(f"**Nivel:** {item['NIVEL_RESULTADO']}")

                with col2:
                    if item["PUNTAJE_ESCALADO"] is not None:
                        st.write(f"**Puntaje escalado:** {item['PUNTAJE_ESCALADO']}")

                    if item["REQUIERE_ATENCION"]:
                        st.warning("Este resultado requiere atención o seguimiento.")
                    else:
                        st.success("Este resultado no refleja alerta alta.")

                st.write("**Interpretación:**")
                st.write(item["INTERPRETACION"])

# ==================================
# SEGUIMIENTO EMOCIONAL
# ==================================
elif selected == "Seguimiento emocional":
    from services.mood_service import MoodService
    import pandas as pd

    st.title("Seguimiento emocional")
    st.write("Registre cómo se siente hoy y lleve un historial de su estado emocional.")

    emotions = MoodService.get_emotions()

    if not emotions:
        st.error("No se pudieron cargar las emociones desde la base de datos.")
    else:
        emotion_map = {
            f"{emotion['NOMBRE_EMOCION']}": emotion["ID_EMOCION"]
            for emotion in emotions
        }

        st.subheader("Registrar estado emocional")

        with st.form("mood_form"):
            emocion_nombre = st.selectbox("Emoción", list(emotion_map.keys()))
            intensidad = st.slider("Intensidad", min_value=1, max_value=5, value=3)
            observacion = st.text_area("Observación", placeholder="Escriba cómo se siente o qué ocurrió hoy...")

            submit_mood = st.form_submit_button("Guardar registro", use_container_width=True)

        if submit_mood:
            ok, message = MoodService.register_mood(
                user["ID_USUARIO"],
                emotion_map[emocion_nombre],
                intensidad,
                observacion
            )

            if ok:
                st.success(message)
            else:
                st.error(message)

        st.divider()
        st.subheader("Historial emocional")

        mood_history = MoodService.get_mood_history(user["ID_USUARIO"])

        if not mood_history:
            st.info("Todavía no hay registros emocionales.")
        else:
            df = pd.DataFrame(mood_history)
            df["FECHA_REGISTRO"] = pd.to_datetime(df["FECHA_REGISTRO"]).dt.strftime("%Y-%m-%d %H:%M")

            st.dataframe(
                df[[
                    "FECHA_REGISTRO",
                    "NOMBRE_EMOCION",
                    "NIVEL_INTENSIDAD",
                    "OBSERVACION"
                ]],
                use_container_width=True
            )

            st.markdown("## Detalle de registros")

            for item in mood_history:
                with st.expander(f"{item['NOMBRE_EMOCION']} - {item['FECHA_REGISTRO']}"):
                    st.write(f"**Emoción:** {item['NOMBRE_EMOCION']}")
                    st.write(f"**Intensidad:** {item['NIVEL_INTENSIDAD']} / 5")
                    st.write(f"**Observación:** {item['OBSERVACION'] if item['OBSERVACION'] else 'Sin observación.'}")

# ==================================
# RECOMENDACIONES
# ==================================
elif selected == "Recomendaciones":
    from services.recommendation_service import RecommendationService

    st.title("Recomendaciones personalizadas")

    st.write("""
    Este módulo genera sugerencias breves y personalizadas de apoyo emocional a partir de:
    - resultados recientes de PHQ-9 y WHO-5
    - edad del usuario
    - último estado emocional registrado
    """)

    st.info("""
    Las recomendaciones tienen un enfoque educativo y de acompañamiento.
    No reemplazan atención profesional.
    """)

    if st.button("Generar recomendaciones con IA", use_container_width=True):
        with st.spinner("Generando recomendaciones..."):
            ok, message, recommendations = RecommendationService.generate_user_recommendations(
                user["ID_USUARIO"]
            )

        if ok:
            st.session_state.recommendations_generated = True
            st.session_state.recommendations_data = recommendations
            st.success(message)
        else:
            st.error(message)

    st.divider()

    if not st.session_state.recommendations_generated or not st.session_state.recommendations_data:
        st.markdown("""
        <div class="recommendation-empty">
            <h3>Aún no se han generado recomendaciones</h3>
            <p>Realice primero sus evaluaciones y luego presione <b>Generar recomendaciones con IA</b>.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.subheader("Recomendaciones generadas")

        for i, rec in enumerate(st.session_state.recommendations_data, start=1):
            titulo = clean_recommendation_text(rec.get("titulo", ""))
            descripcion = clean_recommendation_text(rec.get("descripcion", ""))
            actividad = clean_recommendation_text(rec.get("actividad_diaria", ""))
            ejercicio = clean_recommendation_text(rec.get("ejercicio_guiado", ""))
            meta = clean_recommendation_text(rec.get("meta_semanal", ""))

            with st.container(border=True):
                st.subheader(f"{i}. {titulo}")
                st.write(f"**Descripción:** {descripcion}")
                st.write(f"**Actividad diaria:** {actividad}")
                st.write(f"**Ejercicio guiado:** {ejercicio}")
                st.write(f"**Meta semanal:** {meta}")

        if st.button("Limpiar recomendaciones", use_container_width=True):
            st.session_state.recommendations_generated = False
            st.session_state.recommendations_data = []
            st.rerun()

# ==================================
# PROGRESO Y REPORTES
# ==================================
elif selected == "Progreso y reportes":
    from services.report_service import ReportService
    from services.pdf_report_service import PDFReportService

    st.title("Progreso y reportes")
    st.write("Este módulo muestra el avance del usuario a lo largo del tiempo.")

    summary = ReportService.get_progress_summary(user["ID_USUARIO"])

    if not summary["data"]:
        st.info("Todavía no hay suficientes evaluaciones para mostrar progreso.")
    else:

        st.subheader("Resumen del estado actual")

        col1, col2 = st.columns(2)

        with col1:

            if summary["last_phq9"]:
                st.metric(
                    "Último PHQ-9",
                    summary["last_phq9"]["PUNTAJE_TOTAL"]
                )

        with col2:

            if summary["last_who5"]:
                st.metric(
                    "Último WHO-5",
                    summary["last_who5"]["PUNTAJE_ESCALADO"]
                )

        st.divider()

        st.subheader("Comparación de progreso")

        col1, col2 = st.columns(2)

        with col1:

            if summary["first_phq9"] and summary["last_phq9"]:

                cambio = summary["last_phq9"]["PUNTAJE_TOTAL"] - summary["first_phq9"]["PUNTAJE_TOTAL"]

                st.metric(
                    "Cambio PHQ-9",
                    summary["last_phq9"]["PUNTAJE_TOTAL"],
                    delta=cambio
                )

        with col2:

            if summary["first_who5"] and summary["last_who5"]:

                cambio = summary["last_who5"]["PUNTAJE_ESCALADO"] - summary["first_who5"]["PUNTAJE_ESCALADO"]

                st.metric(
                    "Cambio WHO-5",
                    summary["last_who5"]["PUNTAJE_ESCALADO"],
                    delta=cambio
                )

        st.divider()

        st.subheader("Último estado emocional")

        mood = summary["latest_mood"]

        if mood:
            st.write(f"**Emoción:** {mood['NOMBRE_EMOCION']}")
            st.write(f"**Intensidad:** {mood['NIVEL_INTENSIDAD']} / 5")

            if mood["OBSERVACION"]:
                st.write(f"**Observación:** {mood['OBSERVACION']}")
        else:
            st.info("No hay registros emocionales recientes.")

        st.divider()

        st.divider()
        st.subheader("Reporte descargable")

        if st.button("Generar reporte PDF", use_container_width=True):
            ok, message, pdf_path = PDFReportService.generate_pdf_report(user["ID_USUARIO"])

            if ok:
                st.success(message)

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Descargar reporte PDF",
                        data=pdf_file,
                        file_name="reporte_usuario.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error(message)
# ==================================
# CONFIGURACIÓN
# ==================================
elif selected == "Configuración":
    from services.profile_service import ProfileService

    st.title("Configuración del usuario")
    st.write("Consulte y actualice su información básica.")

    profile = ProfileService.get_profile(user["ID_USUARIO"])

    if not profile:
        st.error("No se pudo cargar la información del usuario.")
    else:
        st.subheader("Información actual")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Cédula:** {profile['CEDULA']}")
            st.write(f"**Correo:** {profile['CORREO']}")
            st.write(f"**Sexo:** {profile['SEXO']}")
            st.write(f"**Rol:** {profile['NOMBRE_ROL']}")

        with col2:
            st.write(f"**Fecha de nacimiento:** {profile['FECHA_NACIMIENTO']}")
            st.write(f"**Nombre actual:** {profile['NOMBRE']}")
            st.write(f"**Apellido actual:** {profile['APELLIDO']}")
            st.write(f"**Usuario actual:** {profile['USERNAME']}")

        st.divider()
        st.subheader("Editar información")

        with st.form("profile_form"):
            nombre = st.text_input("Nombre", value=profile["NOMBRE"])
            apellido = st.text_input("Apellido", value=profile["APELLIDO"])
            telefono = st.text_input("Teléfono", value=profile["TELEFONO"] if profile["TELEFONO"] else "")
            username = st.text_input("Nombre de usuario", value=profile["USERNAME"])

            save_profile = st.form_submit_button("Guardar cambios", use_container_width=True)

        if save_profile:
            ok, message = ProfileService.update_profile(
                user["ID_USUARIO"],
                nombre,
                apellido,
                telefono,
                username
            )

            if ok:
                st.success(message)

                # Refrescar sesión para que el sidebar también se actualice
                updated_profile = ProfileService.get_profile(user["ID_USUARIO"])
                if updated_profile:
                    st.session_state.user["NOMBRE"] = updated_profile["NOMBRE"]
                    st.session_state.user["APELLIDO"] = updated_profile["APELLIDO"]
                    st.session_state.user["USERNAME"] = updated_profile["USERNAME"]
                    st.session_state.user["TELEFONO"] = updated_profile["TELEFONO"]

                st.rerun()
            else:
                st.error(message)

# ==================================
# CERRAR SESIÓN
# ==================================
elif selected == "Cerrar sesión":
    logout()
    st.success("Sesión cerrada correctamente.")
    st.switch_page("pages/login.py")