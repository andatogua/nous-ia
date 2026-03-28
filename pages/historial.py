import streamlit as st
from ui.styles import load_styles
from ui.sidebar import render_sidebar
from ui.components import render_page_header, render_info_box
from utils.session_manager import initialize_session

st.set_page_config(
    page_title="NousIA - Historial",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
initialize_session()

if not st.session_state.user:
    st.switch_page("pages/login.py")

user = st.session_state.user
full_name = f"{user['NOMBRE']} {user['APELLIDO']}"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Historial"

selected = render_sidebar(full_name)

if selected != st.session_state.current_page and selected is not None:
    st.session_state.current_page = selected

selected = st.session_state.current_page

if selected == "Historial":
    pass
elif selected == "Cerrar sesión":
    from utils.session_manager import logout
    logout()
    st.success("Sesión cerrada correctamente.")
    st.switch_page("pages/login.py")
else:
    st.switch_page("pages/dashboard.py")

from services.history_service import HistoryService
import pandas as pd

render_page_header("Historial de evaluaciones", "Consulte todas sus evaluaciones realizadas", "📜")

history = HistoryService.get_user_history(user["ID_USUARIO"])

if not history:
    render_info_box("Todavía no hay evaluaciones registradas. Complete su primera evaluación en el módulo correspondiente.")
else:
    df = pd.DataFrame(history)
    df["FECHA"] = pd.to_datetime(df["FECHA_FIN"]).dt.strftime("%d/%m/%Y")
    df = df.sort_values("FECHA_FIN", ascending=False)
    
    col1, col2, col3 = st.columns(3)
    
    total = len(df)
    phq_count = len(df[df["CUESTIONARIO"].str.contains("Patient Health Questionnaire-9|PHQ-9", case=False, na=False)])
    who_count = len(df[df["CUESTIONARIO"].str.contains("WHO-5|Well-Being", case=False, na=False)])
    
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("PHQ-9", phq_count)
    with col3:
        st.metric("WHO-5", who_count)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h4 style="color: #52b44a; margin-bottom: 1rem;">Detalle de evaluaciones</h4>
    """, unsafe_allow_html=True)
    
    for _, item in df.iterrows():
        nivel = item["NIVEL_RESULTADO"]
        
        if "Severa" in nivel:
            color = "#FEF2F2"
            border = "#EF4444"
        elif "Moderada" in nivel:
            color = "#FFFBEB"
            border = "#F59E0B"
        elif "Bajo" in nivel:
            color = "#FEF2F2"
            border = "#EF4444"
        else:
            color = "#ECFDF5"
            border = "#10B981"
        
        st.markdown(f"""
        <div style="
            background-color: {color};
            border-left: 4px solid {border};
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h5 style="margin: 0; color: #1F2937;">{item['CUESTIONARIO']}</h5>
                <span style="font-size: 0.85rem; color: #6B7280;">{item['FECHA']}</span>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: #4B5563;">
                <strong>Puntaje:</strong> {item['PUNTAJE_TOTAL']} | <strong>Nivel:</strong> {nivel}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
