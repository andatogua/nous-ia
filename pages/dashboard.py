import re
import streamlit as st
from ui.styles import load_styles
from ui.sidebar import render_sidebar
from ui.components import render_page_header, render_section_header, render_info_box, render_warning_box
from utils.session_manager import initialize_session, logout

st.set_page_config(
    page_title="NousIA - Panel principal",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
initialize_session()
print(st.session_state)

if not st.session_state.user:
    st.switch_page("pages/login.py")

user = st.session_state.user
full_name = f"{user['NOMBRE']} {user['APELLIDO']}"

def clean_recommendation_text(text):
    if not text:
        return ""
    text = str(text)
    text = text.replace("```html", "").replace("```json", "").replace("```markdown", "").replace("```", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text).strip()
    return text

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

if "current_page" not in st.session_state:
    st.session_state.current_page = "Datos informativos"

selected = render_sidebar(full_name)

if selected != st.session_state.current_page and selected is not None:
    st.session_state.current_page = selected

selected = st.session_state.current_page

if selected == "Historial":
    st.switch_page("pages/historial.py")

if selected == "Cerrar sesión":
    logout()
    st.success("Sesión cerrada correctamente.")
    st.switch_page("pages/login.py")

if selected == "Datos informativos":
    
    st.image("assets/BannerSuperior.png", width="content")
    # render_page_header(
    #     "Bienvenido a NousIA",
    #     "Explore información sobre el sistema y conceptos de salud emocional",
    #     "🧠"
    # )
    
    st.markdown("""
    <div class="card" style="margin-bottom: 1.5rem;">
        <h3 style="color: #52b44a; margin-bottom: 1rem;">¿Qué es NousIA?</h3>
        <p style="color: #4B5563; line-height: 1.7; margin: 0;">
            NousIA es una aplicación web de apoyo educativo orientada a la detección inicial y autogestión 
            de síntomas relacionados con la depresión. Su propósito es brindar una experiencia digital clara, 
            accesible y útil para que el usuario conozca mejor su estado emocional y pueda dar seguimiento a su bienestar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">📊 Cuestionarios disponibles</h4>
            <p style="margin-bottom: 1rem;"><strong>PHQ-9:</strong> Cuestionario de 9 preguntas para identificar síntomas depresivos.</p>
            <p><strong>WHO-5:</strong> Escala de 5 preguntas que mide el bienestar emocional general.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">📋 Funcionalidades</h4>
            <ul style="color: #4B5563; line-height: 1.8;">
                <li>Realizar evaluaciones de salud emocional</li>
                <li>Registrar estados emocionales</li>
                <li>Visualizar estadísticas e historial</li>
                <li>Recibir recomendaciones personalizadas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style="border-left: 4px solid #52b44a;">
        <h4 style="color: #52b44a; margin-bottom: 1rem;">📖 ¿Qué es la depresión?</h4>
        <p style="color: #4B5563; line-height: 1.7; margin: 0;">
            La depresión es un trastorno del estado de ánimo que afecta la forma en que una persona piensa, 
            siente y actúa. Se manifiesta mediante síntomas emocionales, físicos y cognitivos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="mini-card">
            <h5 style="color: #52b44a; margin-bottom: 0.75rem;">Síntomas frecuentes</h5>
            <ul style="color: #4B5563; line-height: 1.8; margin: 0; padding-left: 1.25rem;">
                <li>Tristeza persistente</li>
                <li>Sensación de vacío</li>
                <li>Cansancio o falta de energía</li>
                <li>Pérdida de interés en actividades</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="mini-card">
            <h5 style="color: #52b44a; margin-bottom: 0.75rem;">Más síntomas</h5>
            <ul style="color: #4B5563; line-height: 1.8; margin: 0; padding-left: 1.25rem;">
                <li>Alteraciones del sueño</li>
                <li>Cambios en el apetito</li>
                <li>Dificultad para concentrarse</li>
                <li>Pensamientos negativos frecuentes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    ">
        <strong>⚠️ Importante:</strong> Este sistema no reemplaza a un profesional de salud mental. Los resultados son orientativos.
    </div>
    """, unsafe_allow_html=True)


elif selected == "Estadísticas":
    from services.statistics_service import StatisticsService
    from services.report_service import ReportService
    from services.pdf_report_service import PDFReportService
    import pandas as pd
    import plotly.express as px
    
    render_page_header("Estadísticas", "Visualice su evolución y progreso emocional", "📊")
    
    stats = StatisticsService.get_user_statistics(user["ID_USUARIO"])
    
    if stats["total"] == 0:
        render_info_box("Todavía no hay evaluaciones para mostrar estadísticas. Realice su primera evaluación en el módulo correspondiente.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Evaluaciones totales", stats["total"])
        with col2:
            st.metric("Promedio PHQ-9", f"{stats['avg_phq']:.1f}")
        with col3:
            st.metric("Promedio WHO-5", f"{stats['avg_who']:.1f}")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        df = pd.DataFrame(stats["data"])
        df["FECHA_FIN"] = pd.to_datetime(df["FECHA_FIN"])
        df["FECHA_GRAFICA"] = df["FECHA_FIN"].dt.strftime("%d/%m/%Y")
        
        st.markdown("""
        <div class="card">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">📈 Evolución de resultados</h4>
        """, unsafe_allow_html=True)
        
        fig = px.line(
            df,
            x="FECHA_GRAFICA",
            y="PUNTAJE_TOTAL",
            color="CODIGO",
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Fecha de evaluación",
            yaxis_title="Puntaje obtenido",
            legend_title="Cuestionario",
            hovermode="x unified",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            last_phq = df[df["CODIGO"] == "PHQ-9"].sort_values("FECHA_FIN").tail(1)
            if not last_phq.empty:
                nivel_phq = last_phq.iloc[0]["NIVEL_RESULTADO"]
                
                if "Severa" in nivel_phq:
                    badge_type = "danger"
                elif "Moderada" in nivel_phq:
                    badge_type = "warning"
                else:
                    badge_type = "success"
                
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: #52b44a; margin-bottom: 1rem;">PHQ-9</h4>
                    <p style="margin: 0;"><strong>Nivel actual:</strong> <span class="badge badge-{badge_type}">{nivel_phq}</span></p>
                    <p style="margin: 0.5rem 0 0 0;"><strong>Puntaje:</strong> {last_phq.iloc[0]["PUNTAJE_TOTAL"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            last_who = df[df["CODIGO"] == "WHO-5"].sort_values("FECHA_FIN").tail(1)
            if not last_who.empty:
                nivel_who = last_who.iloc[0]["NIVEL_RESULTADO"]
                
                if "Bajo" in nivel_who:
                    badge_type = "danger"
                elif "Medio" in nivel_who:
                    badge_type = "warning"
                else:
                    badge_type = "success"
                
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: #52b44a; margin-bottom: 1rem;">WHO-5</h4>
                    <p style="margin: 0;"><strong>Nivel actual:</strong> <span class="badge badge-{badge_type}">{nivel_who}</span></p>
                    <p style="margin: 0.5rem 0 0 0;"><strong>Puntaje:</strong> {last_who.iloc[0]["PUNTAJE_ESCALADO"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">📋 Reporte descargable</h4>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Generar reporte PDF", use_container_width=True):
            with st.spinner("Generando reporte..."):
                ok, message, pdf_path = PDFReportService.generate_pdf_report(user["ID_USUARIO"])
            
            if ok:
                st.success(message)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ Descargar reporte",
                        data=pdf_file,
                        file_name="reporte_usuario.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error(message)
        
        st.markdown("</div>", unsafe_allow_html=True)


elif selected == "Evaluaciones":
    from services.evaluation_service import EvaluationService
    
    render_page_header("Evaluaciones", "Complete los cuestionarios para evaluar su bienestar emocional", "📝")
    
    can_start, availability_message, next_date, days_remaining = EvaluationService.check_evaluation_availability(
        user["ID_USUARIO"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">PHQ-9</h4>
            <p style="color: #4B5563; margin-bottom: 0.5rem;">Cuestionario de 9 preguntas</p>
            <p style="color: #4B5563; margin: 0; font-size: 0.9rem;">Evalúa la presencia y severidad de síntomas depresivos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">WHO-5</h4>
            <p style="color: #4B5563; margin-bottom: 0.5rem;">Escala de 5 preguntas</p>
            <p style="color: #4B5563; margin: 0; font-size: 0.9rem;">Mide el bienestar emocional general del usuario.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    if st.session_state.evaluation_step == "intro":
        if not can_start:
            render_warning_box(availability_message)
            if next_date:
                st.info(f"Faltan aproximadamente {days_remaining} día(s) para habilitar una nueva evaluación.")
        else:
            render_info_box("Responda con sinceridad. Esta evaluación es de apoyo educativo y no sustituye atención profesional.")
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            if st.button("🚀 Comenzar evaluación", type="primary", use_container_width=True):
                st.session_state.evaluation_step = "phq9"
                st.rerun()
    
    elif st.session_state.evaluation_step == "phq9":
        st.markdown("""
        <div style="
            background-color: #F0FDFA;
            border-left: 4px solid #52b44a;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        ">
            <strong>PHQ-9</strong> — Responda cada pregunta según cómo se ha sentido en las últimas 2 semanas.
        </div>
        """, unsafe_allow_html=True)
        
        questionnaire, questions, options = EvaluationService.get_questionnaire_data("PHQ-9")
        
        if not questionnaire or not questions or not options:
            st.error("No se pudo cargar el cuestionario PHQ-9.")
        else:
            with st.form("form_phq9"):
                selected_answers = []
                
                for question in questions:
                    question_id = question["ID_PREGUNTA"]
                    question_options = [opt for opt in options if opt["ID_PREGUNTA"] == question_id]
                    option_map = {
                        opt["ID_OPCION"]: {"texto": opt["TEXTO_OPCION"], "valor": opt["VALOR"]}
                        for opt in question_options
                    }
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 8px; border: 1px solid #E5E7EB;">
                        <p style="font-weight: 600; margin: 0 0 0.75rem 0;">{question['ORDEN_PREGUNTA']}. {question['TEXTO_PREGUNTA']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if option_map:
                        selected_option_id = st.radio(
                            "Seleccione una opción:",
                            options=list(option_map.keys()),
                            format_func=lambda x, om=option_map: om[x]["texto"],
                            key=f"phq9_{question_id}",
                            label_visibility="collapsed"
                        )
                        
                        selected_answers.append({
                            "id_pregunta": question_id,
                            "id_opcion": selected_option_id,
                            "valor": option_map[selected_option_id]["valor"]
                        })
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                enviar_phq9 = st.form_submit_button("Siguiente: WHO-5 →", use_container_width=True)
            
            if enviar_phq9:
                ok, message, result_data = EvaluationService.save_single_evaluation(
                    user["ID_USUARIO"], "PHQ-9", selected_answers
                )
                
                if ok:
                    st.session_state.phq9_score = result_data["puntaje_total"]
                    st.session_state.evaluation_step = "who5"
                    st.success("PHQ-9 guardado correctamente.")
                    st.rerun()
                else:
                    st.error(message)
    
    elif st.session_state.evaluation_step == "who5":
        st.markdown("""
        <div style="
            background-color: #F0FDFA;
            border-left: 4px solid #52b44a;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        ">
            <strong>WHO-5</strong> — Responda cada pregunta según cómo se ha sentido recientemente.
        </div>
        """, unsafe_allow_html=True)
        
        questionnaire, questions, options = EvaluationService.get_questionnaire_data("WHO-5")
        
        if not questionnaire or not questions or not options:
            st.error("No se pudo cargar el cuestionario WHO-5.")
        else:
            with st.form("form_who5"):
                selected_answers = []
                
                for question in questions:
                    question_id = question["ID_PREGUNTA"]
                    question_options = [opt for opt in options if opt["ID_PREGUNTA"] == question_id]
                    option_map = {
                        opt["ID_OPCION"]: {"texto": opt["TEXTO_OPCION"], "valor": opt["VALOR"]}
                        for opt in question_options
                    }
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 8px; border: 1px solid #E5E7EB;">
                        <p style="font-weight: 600; margin: 0 0 0.75rem 0;">{question['ORDEN_PREGUNTA']}. {question['TEXTO_PREGUNTA']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if option_map:
                        selected_option_id = st.radio(
                            "Seleccione una opción:",
                            options=list(option_map.keys()),
                            format_func=lambda x, om=option_map: om[x]["texto"],
                            key=f"who5_{question_id}",
                            label_visibility="collapsed"
                        )
                        
                        selected_answers.append({
                            "id_pregunta": question_id,
                            "id_opcion": selected_option_id,
                            "valor": option_map[selected_option_id]["valor"]
                        })
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                enviar_who5 = st.form_submit_button("Finalizar evaluación", use_container_width=True)
            
            if enviar_who5:
                ok, message, result_data = EvaluationService.save_single_evaluation(
                    user["ID_USUARIO"], "WHO-5", selected_answers
                )
                
                if ok:
                    st.session_state.who5_score = result_data["puntaje_total"]
                    st.session_state.evaluation_step = "results"
                    st.success("WHO-5 guardado correctamente.")
                    st.rerun()
                else:
                    st.error(message)
    
    elif st.session_state.evaluation_step == "results":
        phq9 = st.session_state.phq9_score
        who5 = st.session_state.who5_score
        who5_escalado = who5 * 4 if who5 is not None else 0
        
        render_page_header("Resultados de la evaluación", "Aquí puede ver el resumen de sus evaluaciones", "✅")
        
        col1, col2 = st.columns(2)
        
        with col1:
            phq_level = "Mínima" if phq9 <= 4 else "Leve" if phq9 <= 9 else "Moderada" if phq9 <= 14 else "Moderadamente severa" if phq9 <= 19 else "Severa"
            
            if "Severa" in phq_level:
                result_class = "danger"
            elif "Moderada" in phq_level:
                result_class = "warning"
            else:
                result_class = "success"
            
            st.markdown(f"""
            <div class="card">
                <h4 style="color: #52b44a; margin-bottom: 1rem;">📋 PHQ-9</h4>
                <p style="font-size: 2rem; font-weight: 700; color: #52b44a; margin: 0;">{phq9 if phq9 else 0}</p>
                <p style="margin: 0.5rem 0;"><span class="badge badge-{result_class}">{phq_level}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            who_level = "Bienestar alto" if who5_escalado >= 80 else "Bienestar medio" if who5_escalado >= 52 else "Bienestar bajo"
            
            if "Bajo" in who_level:
                result_class = "danger"
            elif "Medio" in who_level:
                result_class = "warning"
            else:
                result_class = "success"
            
            st.markdown(f"""
            <div class="card">
                <h4 style="color: #52b44a; margin-bottom: 1rem;">💚 WHO-5</h4>
                <p style="font-size: 2rem; font-weight: 700; color: #52b44a; margin: 0;">{who5_escalado}</p>
                <p style="margin: 0.5rem 0;"><span class="badge badge-{result_class}">{who_level}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if phq9 is not None and (phq9 >= 10 or who5_escalado < 52):
            render_warning_box("Los resultados sugieren dar seguimiento al estado emocional. Considere orientación profesional si los síntomas persisten.")
        else:
            st.markdown("""
            <div style="
                background-color: #ECFDF5;
                border-left: 4px solid #10B981;
                padding: 1rem;
                border-radius: 8px;
            ">
                <strong>✓ Buena noticia:</strong> Los resultados no reflejan señales elevadas en este momento. Mantenga hábitos de autocuidado.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Realizar nuevamente", use_container_width=True):
                st.session_state.evaluation_step = "intro"
                st.session_state.phq9_score = None
                st.session_state.who5_score = None
                st.rerun()
        with col_b:
            if st.button("📋 Ver historial", use_container_width=True):
                st.session_state.evaluation_step = "intro"
                st.switch_page("pages/historial.py")


elif selected == "Seguimiento emocional":
    from services.mood_service import MoodService
    from services.activity_service import ActivityService
    from models.recommendation import EstadoRecomendacion
    import pandas as pd
    
    render_page_header("Seguimiento emocional", "Registre y haga seguimiento de sus actividades", "📈")
    
    emotions = MoodService.get_emotions()
    
    if emotions:
        emotion_map = {f"{emotion['NOMBRE_EMOCION']}": emotion["ID_EMOCION"] for emotion in emotions}
    else:
        emotion_map = {}
    
    progress = ActivityService.get_activity_progress_summary(user["ID_USUARIO"])
    activities = ActivityService.get_user_recommended_activities(user["ID_USUARIO"])
    
    if not activities:
        render_info_box("Primero debe generar recomendaciones para habilitar el seguimiento de actividades.")
    else:
        approved_count = sum(1 for a in activities if a.get("ESTADO", "PENDIENTE") == EstadoRecomendacion.APROBADO)
        pending_count = sum(1 for a in activities if a.get("ESTADO", "PENDIENTE") == EstadoRecomendacion.PENDIENTE)
        
        if pending_count > 0:
            st.markdown(f"""
            <div style="
                background-color: #FEF3C7;
                border: 1px solid #F59E0B;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1.5rem;
            ">
                <p style="margin: 0; color: #92400E; font-size: 0.9rem;">
                    <span style="margin-right: 0.5rem;">⚠️</span>
                    <b>{pending_count}</b> recomendación(es) están <b>pendientes de aprobación</b> por un especialista.
                    El seguimiento emocional estará disponible una vez sean aprobadas.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total", progress["total"])
        with col2:
            st.metric("Aprobadas", approved_count)
        with col3:
            st.metric("Pendientes", pending_count)
        with col4:
            st.metric("Cumplimiento", f"{progress['porcentaje_cumplimiento']:.0f}%")
        
        st.progress(progress["porcentaje_cumplimiento"] / 100)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        for i, activity in enumerate(activities, start=1):
            ya_registrada = activity.get("ya_registrada", False)
            estado = activity.get("ESTADO", EstadoRecomendacion.PENDIENTE)
            is_approved = estado == EstadoRecomendacion.APROBADO
            is_rejected = estado == EstadoRecomendacion.RECHAZADO
            is_pending = estado == EstadoRecomendacion.PENDIENTE
            
            estado_color = EstadoRecomendacion.get_color(estado)
            estado_label = EstadoRecomendacion.get_label(estado)
            estado_icon = EstadoRecomendacion.get_icon(estado)
            
            card_bg = "#F3F4F6" if (is_pending or is_rejected) and not ya_registrada else "white"
            border_color = estado_color if (is_pending or is_rejected) and not ya_registrada else "#52b44a"
            
            st.markdown(f"""
            <div class="card" style="margin-bottom: 1rem; background-color: {card_bg}; border-left: 4px solid {border_color};">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <span style="background-color: {border_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600;">{i}</span>
                        <h4 style="margin: 0.5rem 0 0 0; display: inline-block;">{activity['titulo']}</h4>
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <span style="
                            background-color: {estado_color}20;
                            color: {estado_color};
                            padding: 0.25rem 0.75rem;
                            border-radius: 12px;
                            font-size: 0.75rem;
                            font-weight: 600;
                        ">{estado_icon} {estado_label}</span>
                        {('<span class="badge badge-success">Completada</span>' if ya_registrada else '<span class="badge badge-warning">Pendiente</span>' if is_approved else '<span></span>')}
                    </div>
                </div>
                <p style="color: #4B5563; margin-bottom: 1rem;">{activity['actividad']}</p>
            """, unsafe_allow_html=True)
            
            if is_rejected:
                st.markdown("""
                <div style="background-color: #FEE2E2; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="margin: 0; color: #DC2626; font-size: 0.9rem;">
                        <span style="margin-right: 0.5rem;">❌</span>
                        <b>Recomendación rechazada.</b> Esta actividad no está disponible. Comuníquese con su especialista.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif is_pending and not ya_registrada:
                st.markdown("""
                <div style="background-color: #FEF3C7; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="margin: 0; color: #92400E; font-size: 0.9rem;">
                        <span style="margin-right: 0.5rem;">⏳</span>
                        <b>Pendiente de aprobación.</b> El seguimiento emocional estará disponible una vez un especialista apruebe esta recomendación.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                emocion_key = f"emocion_{activity['id_recomendacion']}"
                intensidad_key = f"intensidad_{activity['id_recomendacion']}"
                observacion_key = f"observacion_{activity['id_recomendacion']}"
                realizada_key = f"realizada_{activity['id_recomendacion']}"
                
                if emocion_key not in st.session_state:
                    st.session_state[emocion_key] = activity.get("emocion_guardada") or list(emotion_map.keys())[0] if emotion_map else ""
                if intensidad_key not in st.session_state:
                    st.session_state[intensidad_key] = activity.get("intensidad_guardada", 3)
                if observacion_key not in st.session_state:
                    st.session_state[observacion_key] = activity.get("observacion_guardada") or ""
                if realizada_key not in st.session_state:
                    st.session_state[realizada_key] = "Sí" if activity.get("realizada") in [True, 1] else "No"
                
                with st.form(f"activity_form_{activity['id_recomendacion']}"):
                    col_e, col_i = st.columns(2)
                    emocion_nombre = ""
                    
                    with col_e:
                        if emotion_map:
                            emocion_nombre = st.selectbox(
                                "¿Cómo se sintió?",
                                options=list(emotion_map.keys()),
                                key=emocion_key,
                                disabled=ya_registrada
                            )
                    
                    with col_i:
                        intensidad = st.slider(
                            "Intensidad",
                            min_value=1,
                            max_value=5,
                            key=intensidad_key,
                            disabled=ya_registrada
                        )
                    
                    observacion = st.text_area(
                        "Observación",
                        placeholder="¿Cómo se sintió al realizar esta actividad?",
                        key=observacion_key,
                        disabled=ya_registrada
                    )
                    
                    realizada = st.radio(
                        "¿La realizó?",
                        options=["Sí", "No"],
                        horizontal=True,
                        key=realizada_key,
                        disabled=ya_registrada
                    )
                    
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    
                    save_activity = st.form_submit_button(
                        "✅ Guardado" if ya_registrada else "Guardar actividad",
                        use_container_width=True,
                        disabled=ya_registrada
                    )
                
                if save_activity and not ya_registrada:
                    ok_tracking, message_tracking = ActivityService.save_activity_emotional_tracking(
                        user["ID_USUARIO"],
                        activity["id_recomendacion"],
                        emotion_map.get(emocion_nombre, 1),
                        intensidad,
                        observacion,
                        True if realizada == "Sí" else False
                    )
                    
                    if ok_tracking:
                        st.success("Actividad guardada correctamente.")
                        st.rerun()
                    else:
                        st.error(message_tracking)
            
            st.markdown("</div>", unsafe_allow_html=True)


elif selected == "Recomendaciones":
    from services.recommendation_service import RecommendationService
    from repositories.recommendation_repository import RecommendationRepository
    from models.recommendation import EstadoRecomendacion
    from datetime import datetime
    
    render_page_header("Recomendaciones", "Sugerencias personalizadas basadas en sus evaluaciones", "💡")
    
    st.markdown("""
    <div class="card" style="margin-bottom: 1.5rem;">
        <p style="color: #4B5563; margin: 0;">
            Este módulo genera sugerencias breves y personalizadas de apoyo emocional a partir de sus resultados 
            en PHQ-9, WHO-5, edad y último estado emocional registrado.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn, col_filter = st.columns([2, 1])
    
    with col_btn:
        if st.button("🤖 Generar recomendaciones con IA", type="primary", use_container_width=True):
            with st.spinner("Generando recomendaciones personalizadas..."):
                ok, message, recommendations = RecommendationService.generate_user_recommendations(
                    user["ID_USUARIO"]
                )
            
            if ok:
                st.session_state.recommendations_generated = True
                st.session_state.recommendations_data = recommendations
                st.session_state.recommendation_period = "today"
                st.success("Recomendaciones generadas correctamente.")
            else:
                st.error(message)
    
    with col_filter:
        if "recommendation_period" not in st.session_state:
            st.session_state.recommendation_period = "month"
        
        period = st.selectbox(
            "Filtrar por período:",
            options=["today", "week", "month", "all"],
            format_func=lambda x: {
                "today": "📅 Hoy",
                "week": "📆 Última semana", 
                "month": "📆 Este mes",
                "all": "📋 Todas"
            }[x],
            index=["today", "week", "month", "all"].index(st.session_state.recommendation_period),
            key="period_selector"
        )
        st.session_state.recommendation_period = period
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    recommendations = RecommendationRepository.get_recommendations_by_period(
        user["ID_USUARIO"], 
        period
    )
    
    if not recommendations:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem;
            background-color: white;
            border-radius: 16px;
            border: 2px dashed #E5E7EB;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
            <h3 style="color: #6B7280; margin-bottom: 0.5rem;">Sin recomendaciones</h3>
            <p style="color: #9CA3AF;">No hay recomendaciones para el período seleccionado. Genere nuevas con el botón de arriba.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        pending_count = sum(1 for rec in recommendations if rec.get("ESTADO", "PENDIENTE") == EstadoRecomendacion.PENDIENTE)
        rejected_count = sum(1 for rec in recommendations if rec.get("ESTADO", "PENDIENTE") == EstadoRecomendacion.RECHAZADO)
        
        if pending_count > 0 or rejected_count > 0:
            alert_messages = []
            if pending_count > 0:
                alert_messages.append(f"<b>{pending_count}</b> recomendación(es) están <b>pendientes de aprobación</b> por un especialista")
            if rejected_count > 0:
                alert_messages.append(f"<b>{rejected_count}</b> recomendación(es) fueron <b>rechazadas</b>")
            
            alert_text = " y ".join(alert_messages)
            alert_text += ". El seguimiento emocional estará disponible una vez sean aprobadas."
            
            st.markdown(f"""
            <div style="
                background-color: #FEF3C7;
                border: 1px solid #F59E0B;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1.5rem;
            ">
                <p style="margin: 0; color: #92400E;">
                    <span style="margin-right: 0.5rem;">⚠️</span>
                    {alert_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        grouped = {}
        for rec in recommendations:
            fecha = rec["FECHA_GENERACION"]
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
            
            date_key = fecha.strftime("%Y-%m-%d")
            date_label = fecha.strftime("%d %b %Y")
            
            if date_key not in grouped:
                grouped[date_key] = {"label": date_label, "items": []}
            grouped[date_key]["items"].append(rec)
        
        total_count = 0
        for date_key in sorted(grouped.keys(), reverse=True):
            group = grouped[date_key]
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1.5rem 0 0.75rem 0;">
                <span style="font-size: 1.2rem;">📅</span>
                <h3 style="margin: 0; color: #1F2937;">{group['label']}</h3>
                <span style="
                    background-color: #E5E7EB;
                    color: #6B7280;
                    padding: 0.25rem 0.75rem;
                    border-radius: 12px;
                    font-size: 0.85rem;
                    margin-left: 0.5rem;
                ">{len(group['items'])} recomendación(es)</span>
            </div>
            """, unsafe_allow_html=True)
            
            for rec in group['items']:
                total_count += 1
                titulo = clean_recommendation_text(rec.get("TITULO", ""))
                descripcion = clean_recommendation_text(rec.get("DESCRIPCION", ""))
                hora = rec["FECHA_GENERACION"]
                if isinstance(hora, str):
                    hora = datetime.strptime(hora, "%Y-%m-%d %H:%M:%S")
                hora_label = hora.strftime("%H:%M")
                estado = rec.get("ESTADO", EstadoRecomendacion.PENDIENTE)
                
                estado_color = EstadoRecomendacion.get_color(estado)
                estado_label = EstadoRecomendacion.get_label(estado)
                estado_icon = EstadoRecomendacion.get_icon(estado)
                
                accion = ""
                if descripcion and "Acción sugerida:" in descripcion:
                    parts = descripcion.split("Acción sugerida:")
                    descripcion = parts[0].strip()
                    accion = parts[1].strip() if len(parts) > 1 else ""
                
                is_pending = estado == EstadoRecomendacion.PENDIENTE
                is_rejected = estado == EstadoRecomendacion.RECHAZADO
                border_color = "#6B7280" if is_rejected else ("#F59E0B" if is_pending else "#52b44a")
                
                st.markdown(f"""
                <div class="card" style="margin-bottom: 1rem; border-left: 4px solid {border_color}; opacity: {'0.7' if is_rejected else '1'};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="
                                background-color: {border_color};
                                color: white;
                                width: 28px;
                                height: 28px;
                                border-radius: 50%;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 700;
                                font-size: 0.85rem;
                            ">{total_count}</span>
                            <h4 style="margin: 0; color: #1F2937;">{titulo}</h4>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="
                                background-color: {estado_color}20;
                                color: {estado_color};
                                padding: 0.25rem 0.75rem;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 600;
                            ">{estado_icon} {estado_label}</span>
                            <span style="color: #9CA3AF; font-size: 0.85rem;">🕐 {hora_label}</span>
                        </div>
                    </div>
                    <p style="color: #4B5563; margin-bottom: 0.5rem;">{descripcion}</p>
                    {f'''<div style="background-color: #F0FDFA; padding: 0.75rem 1rem; border-radius: 8px;">
                        <p style="margin: 0; color: #52b44a; font-weight: 600;">
                            <span style="margin-right: 0.5rem;">🎯</span>Acción sugerida: {accion}
                        </p>
                    </div>''' if accion else ''}
                    {f'''<div style="background-color: #FEE2E2; padding: 0.5rem 0.75rem; border-radius: 6px; margin-top: 0.5rem;">
                        <p style="margin: 0; color: #DC2626; font-size: 0.85rem;">
                            <span style="margin-right: 0.5rem;">ℹ️</span>Esta recomendación fue rechazada. Comuníquese con su especialista.
                        </p>
                    </div>''' if is_rejected else ''}
                </div>
                """, unsafe_allow_html=True)


elif selected == "Configuración":
    from services.profile_service import ProfileService
    
    render_page_header("Configuración", "Gestione su información personal", "⚙️")
    
    profile = ProfileService.get_profile(user["ID_USUARIO"])
    
    if not profile:
        st.error("No se pudo cargar la información del usuario.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card">
                <h4 style="color: #52b44a; margin-bottom: 1rem;">Información actual</h4>
                <p style="margin: 0.5rem 0;"><strong>Cédula:</strong> {0}</p>
                <p style="margin: 0.5rem 0;"><strong>Correo:</strong> {1}</p>
                <p style="margin: 0.5rem 0;"><strong>Sexo:</strong> {2}</p>
                <p style="margin: 0.5rem 0;"><strong>Rol:</strong> {3}</p>
            </div>
            """.format(profile['CEDULA'], profile['CORREO'], profile['SEXO'], profile['NOMBRE_ROL']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h4 style="color: #52b44a; margin-bottom: 1rem;">Datos personales</h4>
                <p style="margin: 0.5rem 0;"><strong>Nombre:</strong> {0} {1}</p>
                <p style="margin: 0.5rem 0;"><strong>Usuario:</strong> {2}</p>
                <p style="margin: 0.5rem 0;"><strong>Fecha de nacimiento:</strong> {3}</p>
            </div>
            """.format(profile['NOMBRE'], profile['APELLIDO'], profile['USERNAME'], profile['FECHA_NACIMIENTO']), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4 style="color: #52b44a; margin-bottom: 1rem;">Editar información</h4>
        """, unsafe_allow_html=True)
        
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre", value=profile["NOMBRE"])
            
            with col2:
                apellido = st.text_input("Apellido", value=profile["APELLIDO"])
            
            col3, col4 = st.columns(2)
            
            with col3:
                telefono = st.text_input("Teléfono", value=profile["TELEFONO"] if profile["TELEFONO"] else "")
            
            with col4:
                username = st.text_input("Nombre de usuario", value=profile["USERNAME"])
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
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
                updated_profile = ProfileService.get_profile(user["ID_USUARIO"])
                if updated_profile:
                    st.session_state.user["NOMBRE"] = updated_profile["NOMBRE"]
                    st.session_state.user["APELLIDO"] = updated_profile["APELLIDO"]
                    st.session_state.user["USERNAME"] = updated_profile["USERNAME"]
                    st.session_state.user["TELEFONO"] = updated_profile["TELEFONO"]
                st.rerun()
            else:
                st.error(message)
        
        st.markdown("</div>", unsafe_allow_html=True)
