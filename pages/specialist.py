import streamlit as st
import pandas as pd
from services.auth_service import AuthService
from services.statistics_service import StatisticsService
from repositories.recommendation_repository import RecommendationRepository
from repositories.statistics_repository import StatisticsRepository
from models.recommendation import EstadoRecomendacion
from ui.styles import load_styles
from utils.session_manager import initialize_session, logout
from datetime import datetime, date

st.set_page_config(
    page_title="NousIA - Panel del Especialista",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()

st.markdown("""
<style>
    /* Estilos específicos para el Panel del Especialista - COLOR AZUL */
    [data-testid="stSidebar"] .sidebar-brand {
        background: linear-gradient(135deg, #0066cc 0%, #0055aa 100%) !important;
    }
    
    [data-testid="stSidebar"] .sidebar-user-card {
        background: linear-gradient(135deg, #E6F0FF 0%, #CCE0FF 100%) !important;
        border: 1px solid rgba(0, 102, 204, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .sidebar-user-icon {
        background-color: #0066cc !important;
    }
</style>
""", unsafe_allow_html=True)
initialize_session()

if st.session_state.user:
    user = st.session_state.user
    if user.get("ID_ROL") != 3:
        st.error("Acceso denegado. Esta área es solo para especialistas.")
        st.stop()
else:
    st.switch_page("pages/login.py")

user = st.session_state.user
full_name = f"{user['NOMBRE']} {user['APELLIDO']}"

with st.sidebar:
    from streamlit_option_menu import option_menu
    
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">NousIA</div>
        <div class="sidebar-brand-subtitle">Panel del Especialista</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="sidebar-user-card">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="sidebar-user-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                </svg>
            </div>
            <div>
                <div class="sidebar-user-label">Especialista</div>
                <div class="sidebar-user-name">{full_name}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    menu_options = [
        "Dashboard",
        "Gestión de Recomendaciones",
        "Pacientes Recientes",
        "Cerrar sesión"
    ]
    
    menu_icons = [
        "bar-chart-line",
        "clipboard2-check",
        "people",
        "box-arrow-right"
    ]
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent!important",
                "margin-top": "6px"
            },
            "icon": {
                "font-size": "18px",
                "color": "#0066cc!important"
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "3px 0",
                "padding": "10px 14px",
                "border-radius": "10px",
                "color": "#1F2937",
                "font-weight": "500"
            },
            "nav-link-selected": {
                "background-color": "#0066cc!important",
                "color": "white!important",
                "font-weight": "600",
                "border-radius": "10px"
            },
            "nav-link:hover": {
                "background-color": "#E6F0FF"
            }
        },
        key="specialist_menu"
    )
    
    if selected == "Cerrar sesión":
        logout()
        st.switch_page("pages/login.py")
    
    page = selected
st.image("assets/BannerSuperior.png", width="content")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0066cc 0%, #0055aa 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">🏥 Panel del Especialista</h1>
    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Bienvenido, {full_name}. Aquí puede gestionar recomendaciones y visualizar estadísticas.</p>
</div>
""", unsafe_allow_html=True)

if page == "Dashboard":
    with st.spinner("Cargando estadísticas..."):
        stats = StatisticsService.get_global_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Pacientes Registrados", stats["patients"])
    
    with col2:
        st.metric("📋 Total Recomendaciones", stats["recommendations"]["total"])
    
    with col3:
        approved = stats["recommendations"]["approved"]
        total = stats["recommendations"]["total"]
        rate = round((approved / total) * 100, 1) if total > 0 else 0
        st.metric("✅ Tasa de Aprobación", f"{rate}%")
    
    with col4:
        st.metric("📈 Evaluaciones Totales", stats["evaluations"]["total_evaluations"])
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.markdown("""
        <div class="card">
            <h3 style="margin-bottom: 1rem;">📊 Promedio de Evaluaciones</h3>
        </div>
        """, unsafe_allow_html=True)
        
        eval_data = {
            "Prueba": ["PHQ-9", "WHO-5"],
            "Promedio": [stats["evaluations"]["avg_phq"], stats["evaluations"]["avg_who"]]
        }
        eval_df = pd.DataFrame(eval_data).set_index("Prueba")
        st.bar_chart(eval_df)
        
        col_phq, col_who = st.columns(2)
        with col_phq:
            phq_status = "Normal" if stats["evaluations"]["avg_phq"] <= 4 else ("Leve" if stats["evaluations"]["avg_phq"] <= 9 else ("Moderado" if stats["evaluations"]["avg_phq"] <= 14 else "Severo"))
            st.markdown(f"""
            <div style="background-color: #E6F0FF; padding: 1rem; border-radius: 12px; text-align: center;">
                <h4 style="margin: 0; color: #0066cc;">PHQ-9</h4>
                <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #1F2937;">{stats["evaluations"]["avg_phq"]}</p>
                <span style="background-color: {'#10B981' if phq_status == 'Normal' else '#F59E0B' if phq_status in ['Leve', 'Moderado'] else '#EF4444'}; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem;">{phq_status}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_who:
            who_status = "Bueno" if stats["evaluations"]["avg_who"] >= 13 else ("Bajo" if stats["evaluations"]["avg_who"] >= 8 else "Muy bajo")
            st.markdown(f"""
            <div style="background-color: #EFF6FF; padding: 1rem; border-radius: 12px; text-align: center;">
                <h4 style="margin: 0; color: #3B82F6;">WHO-5</h4>
                <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #1F2937;">{stats["evaluations"]["avg_who"]}</p>
                <span style="background-color: {'#10B981' if who_status == 'Bueno' else '#F59E0B' if who_status == 'Bajo' else '#EF4444'}; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem;">{who_status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_graph2:
        st.markdown("""
        <div class="card">
            <h3 style="margin-bottom: 1rem;">😊 Estados Emocionales Más Frecuentes</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if stats["emotions"]:
            emotion_data = {
                "Emoción": [e["NOMBRE_EMOCION"] for e in stats["emotions"]],
                "Cantidad": [e["cantidad"] for e in stats["emotions"]]
            }
            emotion_df = pd.DataFrame(emotion_data)
            st.bar_chart(emotion_df.set_index("Emoción"), color="#0066cc")
        else:
            st.info("No hay datos de emociones registrados aún.")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        st.markdown("""
        <div class="card">
            <h3 style="margin-bottom: 1rem;">📈 Cumplimiento de Actividades</h3>
        </div>
        """, unsafe_allow_html=True)
        
        activity_rate = stats["activity_rate"]
        rate_value = float(activity_rate['rate'])
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <p style="font-size: 3rem; font-weight: 700; margin: 0; color: #0066cc;">{rate_value}%</p>
            <p style="color: #6B7280; margin: 0.5rem 0;">{activity_rate['completed']} de {activity_rate['total']} actividades completadas</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(rate_value / 100)
    
    with col_act2:
        st.markdown("""
        <div class="card">
            <h3 style="margin-bottom: 1rem;">📊 Estado de Recomendaciones</h3>
        </div>
        """, unsafe_allow_html=True)
        
        rec_stats = stats["recommendations"]
        status_data = {
            "Estado": ["Pendientes", "Aprobadas", "Rechazadas"],
            "Cantidad": [rec_stats["pending"], rec_stats["approved"], rec_stats["rejected"]]
        }
        status_df = pd.DataFrame(status_data)
        st.bar_chart(status_df.set_index("Estado"))

elif page == "Gestión de Recomendaciones":
    col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 2])
    
    with col_filter1:
        filter_status = st.selectbox(
            "Estado:",
            options=["", "PENDIENTE", "APROBADO", "RECHAZADO"],
            format_func=lambda x: "Todos" if x == "" else {"PENDIENTE": "⏳ Pendientes", "APROBADO": "✅ Aprobadas", "RECHAZADO": "❌ Rechazadas"}[x],
            index=0
        )
    
    with col_filter2:
        filter_date = st.date_input("Fecha:", value=None)
    
    with col_filter3:
        search_patient = st.text_input("Buscar paciente:", placeholder="Nombre o apellido...")
    
    col_quick1, col_quick2 = st.columns([1, 3])
    
    with col_quick1:
        st.markdown("**Aprobación rápida:**")
        quick_date = st.date_input("Fecha para aprobar:", value=date.today(), label_visibility="collapsed")
        
        if st.button("✅ Aprobar todas de esta fecha", use_container_width=True):
            with st.spinner("Aprobando recomendaciones..."):
                count = RecommendationRepository.update_recommendations_by_date(
                    quick_date.strftime("%Y-%m-%d"),
                    EstadoRecomendacion.APROBADO
                )
            if count > 0:
                st.success(f"Se aprobaron {count} recomendación(es).")
                st.rerun()
            else:
                st.warning("No había recomendaciones pendientes para esa fecha.")
    
    with col_quick2:
        pass
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.spinner("Cargando recomendaciones..."):
        filter_date_str = filter_date.strftime("%Y-%m-%d") if filter_date else None
        recommendations = RecommendationRepository.get_recommendations_for_approval(
            estado=filter_status if filter_status else None,
            fecha=filter_date_str,
            paciente_nombre=search_patient if search_patient else None
        )
    
    if not recommendations:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: white; border-radius: 16px; border: 2px dashed #E5E7EB;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
            <h3 style="color: #6B7280; margin-bottom: 0.5rem;">Sin resultados</h3>
            <p style="color: #9CA3AF;">No se encontraron recomendaciones con los filtros seleccionados.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        grouped = {}
        for rec in recommendations:
            patient_key = rec["ID_USUARIO"]
            if patient_key not in grouped:
                grouped[patient_key] = {
                    "nombre": rec["NOMBRE"],
                    "apellido": rec["APELLIDO"],
                    "correo": rec["CORREO"],
                    "recomendaciones": []
                }
            grouped[patient_key]["recomendaciones"].append(rec)
        
        total_recs = len(recommendations)
        st.markdown(f"**{total_recs}** recomendación(es) encontrada(s) en **{len(grouped)}** paciente(s)")
        
        for patient_id, patient_data in grouped.items():
            pending_count = sum(1 for r in patient_data["recomendaciones"] if r.get("ESTADO") == "PENDIENTE")
            patient_name = f"{patient_data['nombre']} {patient_data['apellido']}"
            
            expander_label = f"👤 {patient_name}"
            if pending_count > 0:
                expander_label += f" - {pending_count} ⏳ pendientes"
            else:
                expander_label += f" - {len(patient_data['recomendaciones'])} recomendación(es)"
            
            with st.expander(expander_label):
                col_header1, col_header2 = st.columns([3, 1])
                
                with col_header1:
                    st.markdown(f"**Correo:** {patient_data['correo']}")
                    st.markdown(f"**Total recomendaciones:** {len(patient_data['recomendaciones'])}")
                
                with col_header2:
                    if pending_count > 0:
                        if st.button(f"✅ Aprobar todas ({pending_count})", key=f"approve_all_{patient_id}", use_container_width=True):
                            st.session_state[f"confirm_approve_{patient_id}"] = True
                
                if st.session_state.get(f"confirm_approve_{patient_id}", False):
                    st.markdown(f"""
                    <div style="background-color: #FEF3C7; border: 1px solid #F59E0B; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                        <p style="margin: 0 0 0.5rem 0; color: #92400E; font-weight: 600;">
                            ⚠️ ¿Está seguro de aprobar las {pending_count} recomendación(es) pendientes de {patient_name}?
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_confirm1, col_confirm2 = st.columns(2)
                    with col_confirm1:
                        if st.button("✅ Confirmar", key=f"confirm_yes_{patient_id}", use_container_width=True):
                            with st.spinner("Aprobando..."):
                                count = 0
                                for rec in patient_data["recomendaciones"]:
                                    if rec.get("ESTADO") == "PENDIENTE":
                                        ok, _ = RecommendationRepository.update_recommendation_status(
                                            rec["ID_RECOMENDACION"],
                                            EstadoRecomendacion.APROBADO
                                        )
                                        if ok:
                                            count += 1
                            st.session_state[f"confirm_approve_{patient_id}"] = False
                            st.success(f"Se aprobaron {count} recomendación(es) de {patient_name}.")
                            st.rerun()
                    
                    with col_confirm2:
                        if st.button("❌ Cancelar", key=f"confirm_no_{patient_id}", use_container_width=True):
                            st.session_state[f"confirm_approve_{patient_id}"] = False
                            st.rerun()
                
                st.markdown("---")
                st.markdown("**Recomendaciones:**")
                
                for rec in patient_data["recomendaciones"]:
                    estado = rec.get("ESTADO", "PENDIENTE")
                    estado_color = EstadoRecomendacion.get_color(estado)
                    estado_label = EstadoRecomendacion.get_label(estado)
                    estado_icon = EstadoRecomendacion.get_icon(estado)
                    
                    fecha = rec["FECHA_GENERACION"]
                    if isinstance(fecha, str):
                        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                    fecha_str = fecha.strftime("%d %b %Y %H:%M")
                    
                    st.markdown(f"""
                    <div style="background-color: {estado_color}10; border-left: 4px solid {estado_color}; padding: 1rem; margin: 0.75rem 0; border-radius: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: #1F2937;">{rec['TITULO'][:80]}</h4>
                            <span style="background-color: {estado_color}20; color: {estado_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                                {estado_icon} {estado_label}
                            </span>
                        </div>
                        <p style="margin: 0.5rem 0; color: #6B7280; font-size: 0.9rem;">{rec['DESCRIPCION'][:150]}...</p>
                        <p style="margin: 0; color: #9CA3AF; font-size: 0.85rem;">📅 {fecha_str}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if estado == "PENDIENTE":
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✅ Aprobar", key=f"approve_{rec['ID_RECOMENDACION']}", use_container_width=True):
                                ok, msg = RecommendationRepository.update_recommendation_status(
                                    rec["ID_RECOMENDACION"],
                                    EstadoRecomendacion.APROBADO
                                )
                                if ok:
                                    st.success("Aprobada")
                                    st.rerun()
                                else:
                                    st.error(msg)
                        
                        with col_action2:
                            if st.button("❌ Rechazar", key=f"reject_{rec['ID_RECOMENDACION']}", use_container_width=True):
                                ok, msg = RecommendationRepository.update_recommendation_status(
                                    rec["ID_RECOMENDACION"],
                                    EstadoRecomendacion.RECHAZADO
                                )
                                if ok:
                                    st.success("Rechazada")
                                    st.rerun()
                                else:
                                    st.error(msg)
                    
                    tracking = RecommendationRepository.get_patient_tracking_history(rec["ID_RECOMENDACION"])
                    if tracking:
                        with st.expander("📊 Ver historial de seguimiento"):
                            for t in tracking:
                                st.markdown(f"- **{t['NOMBRE_EMOCION']}** (Intensidad: {t['NIVEL_INTENSIDAD']}/5) - {t['FECHA_REGISTRO']}")
                                if t.get('OBSERVACION'):
                                    st.markdown(f"  __{t['OBSERVACION']}__")
                    
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

elif page == "Pacientes Recientes":
    st.markdown("""
    <div class="card">
        <h3 style="margin-bottom: 1rem;">👥 Gestión de Pacientes</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_search, col_button = st.columns([4, 1])
    
    with col_search:
        search_term = st.text_input("🔍 Buscar paciente:", placeholder="Buscar por nombre, apellido, correo o cédula...")
    
    with col_button:
        st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)
        search_clicked = st.button("Buscar", use_container_width=True)
    
    if "selected_patient" not in st.session_state:
        st.session_state.selected_patient = None
    
    if search_term or search_clicked:
        with st.spinner("Buscando pacientes..."):
            patients = StatisticsRepository.get_all_patients(search_term if search_term else None)
        
        if not patients:
            st.info("No se encontraron pacientes con ese criterio de búsqueda.")
        else:
            st.markdown(f"**{len(patients)}** paciente(s) encontrado(s)")
            
            for patient in patients:
                patient_id = patient["ID_USUARIO"]
                
                fecha_reg = patient["FECHA_CREACION"]
                if hasattr(fecha_reg, 'strftime'):
                    fecha_str = fecha_reg.strftime("%d %b %Y")
                else:
                    fecha_str = str(fecha_reg) if fecha_reg else "N/A"
                
                with st.expander(f"👤 {patient['NOMBRE']} {patient['APELLIDO']} - {patient['CORREO']}"):
                    col_info1, col_info2 = st.columns([1, 1])
                    
                    with col_info1:
                        st.markdown(f"""
                        <div style="background-color: #E6F0FF; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #0066cc;">📋 Información Personal</h4>
                            <p style="margin: 0.25rem 0;"><strong>Nombre:</strong> {patient['NOMBRE']} {patient['APELLIDO']}</p>
                            <p style="margin: 0.25rem 0;"><strong>Correo:</strong> {patient['CORREO']}</p>
                            <p style="margin: 0.25rem 0;"><strong>Teléfono:</strong> {patient.get('TELEFONO') or 'No registrado'}</p>
                            <p style="margin: 0.25rem 0;"><strong>Sexo:</strong> {patient.get('SEXO') or 'No registrado'}</p>
                            <p style="margin: 0.25rem 0;"><strong>Fecha Nac.:</strong> {patient.get('FECHA_NACIMIENTO') or 'No registrada'}</p>
                            <p style="margin: 0.25rem 0;"><strong>Fecha Registro:</strong> {fecha_str}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_info2:
                        st.markdown(f"""
                        <div style="background-color: #E6F0FF; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #0066cc;">📊 Estadísticas</h4>
                            <p style="margin: 0.25rem 0;"><strong>Total Evaluaciones:</strong> {patient['total_evaluaciones']}</p>
                            <p style="margin: 0.25rem 0;"><strong>Total Recomendaciones:</strong> {patient['total_recomendaciones']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    tab1, tab2, tab3 = st.tabs(["📋 Evaluaciones", "💡 Recomendaciones", "😊 Historial Emocional"])
                    
                    with tab1:
                        evaluations = StatisticsRepository.get_patient_evaluations(patient_id)
                        if not evaluations:
                            st.info("Este paciente no tiene evaluaciones registradas.")
                        else:
                            eval_data = []
                            for ev in evaluations:
                                fecha = ev['FECHA_FIN']
                                if hasattr(fecha, 'strftime'):
                                    fecha_eval = fecha.strftime("%d %b %Y")
                                else:
                                    fecha_eval = str(fecha) if fecha else "N/A"
                                
                                eval_data.append({
                                    "Prueba": ev['CODIGO'],
                                    "Puntaje": ev['PUNTAJE_TOTAL'],
                                    "Puntaje Escalado": ev['PUNTAJE_ESCALADO'] or "N/A",
                                    "Nivel": ev['NIVEL_RESULTADO'],
                                    "Fecha": fecha_eval
                                })
                            
                            st.dataframe(pd.DataFrame(eval_data), use_container_width=True, hide_index=True)
                    
                    with tab2:
                        recommendations = StatisticsRepository.get_patient_recommendations(patient_id)
                        if not recommendations:
                            st.info("Este paciente no tiene recomendaciones generadas.")
                        else:
                            pending = sum(1 for r in recommendations if r.get('ESTADO') == 'PENDIENTE')
                            approved = sum(1 for r in recommendations if r.get('ESTADO') == 'APROBADO')
                            rejected = sum(1 for r in recommendations if r.get('ESTADO') == 'RECHAZADO')
                            
                            col_r1, col_r2, col_r3 = st.columns(3)
                            with col_r1:
                                st.metric("⏳ Pendientes", pending)
                            with col_r2:
                                st.metric("✅ Aprobadas", approved)
                            with col_r3:
                                st.metric("❌ Rechazadas", rejected)
                            
                            st.markdown("---")
                            
                            for rec in recommendations:
                                estado = rec.get('ESTADO', 'PENDIENTE')
                                estado_color = EstadoRecomendacion.get_color(estado)
                                estado_label = EstadoRecomendacion.get_label(estado)
                                estado_icon = EstadoRecomendacion.get_icon(estado)
                                
                                fecha = rec['FECHA_GENERACION']
                                if hasattr(fecha, 'strftime'):
                                    fecha_rec = fecha.strftime("%d %b %Y %H:%M")
                                else:
                                    fecha_rec = str(fecha) if fecha else "N/A"
                                
                                st.markdown(f"""
                                <div style="background-color: {estado_color}10; border-left: 4px solid {estado_color}; padding: 1rem; margin: 0.75rem 0; border-radius: 8px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <h4 style="margin: 0; color: #1F2937;">{rec['TITULO'][:80]}</h4>
                                        <span style="background-color: {estado_color}20; color: {estado_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                                            {estado_icon} {estado_label}
                                        </span>
                                    </div>
                                    <p style="margin: 0.5rem 0; color: #6B7280; font-size: 0.9rem;">{rec['DESCRIPCION'][:150]}...</p>
                                    <p style="margin: 0; color: #9CA3AF; font-size: 0.85rem;">📅 {fecha_rec}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if estado == "PENDIENTE":
                                    col_aprob, col_rech = st.columns(2)
                                    with col_aprob:
                                        if st.button("✅ Aprobar", key=f"pat_approve_{rec['ID_RECOMENDACION']}", use_container_width=True):
                                            ok, msg = RecommendationRepository.update_recommendation_status(
                                                rec['ID_RECOMENDACION'],
                                                EstadoRecomendacion.APROBADO
                                            )
                                            if ok:
                                                st.success("Recomendación aprobada")
                                                st.rerun()
                                            else:
                                                st.error(msg)
                                    
                                    with col_rech:
                                        if st.button("❌ Rechazar", key=f"pat_reject_{rec['ID_RECOMENDACION']}", use_container_width=True):
                                            ok, msg = RecommendationRepository.update_recommendation_status(
                                                rec['ID_RECOMENDACION'],
                                                EstadoRecomendacion.RECHAZADO
                                            )
                                            if ok:
                                                st.success("Recomendación rechazada")
                                                st.rerun()
                                            else:
                                                st.error(msg)
                                
                                tracking = RecommendationRepository.get_patient_tracking_history(rec['ID_RECOMENDACION'])
                                if tracking:
                                    with st.expander("📊 Ver seguimiento"):
                                        for t in tracking:
                                            st.markdown(f"- **{t['NOMBRE_EMOCION']}** (Intensidad: {t['NIVEL_INTENSIDAD']}/5) - {t['FECHA_REGISTRO']}")
                                            if t.get('OBSERVACION'):
                                                st.markdown(f"  __{t['OBSERVACION']}__")
                    
                    with tab3:
                        emotional_history = StatisticsRepository.get_patient_emotional_history(patient_id)
                        if not emotional_history:
                            st.info("Este paciente no tiene historial emocional registrado.")
                        else:
                            emotion_data = []
                            for entry in emotional_history:
                                fecha = entry['FECHA_REGISTRO']
                                if hasattr(fecha, 'strftime'):
                                    fecha_hist = fecha.strftime("%d %b %Y %H:%M")
                                else:
                                    fecha_hist = str(fecha) if fecha else "N/A"
                                
                                emotion_data.append({
                                    "Fecha": fecha_hist,
                                    "Emoción": entry['NOMBRE_EMOCION'],
                                    "Intensidad": f"{entry['NIVEL_INTENSIDAD']}/5",
                                    "Actividad Realizada": "Sí" if entry['REALIZADA'] else "No",
                                    "Recomendación": entry['RECOMENDACION_TITULO'][:50] + "..." if entry.get('RECOMENDACION_TITULO') else "N/A",
                                    "Observación": entry.get('OBSERVACION') or "Sin observación"
                                })
                            
                            st.dataframe(pd.DataFrame(emotion_data), use_container_width=True, hide_index=True)
