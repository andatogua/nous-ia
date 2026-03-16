import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar(user_name: str):
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-user-box">
            <div class="sidebar-user-icon">👤</div>
            <div>
                <div class="sidebar-user-label">Usuario conectado</div>
                <div class="sidebar-user-name">{user_name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-brand-card">
            <div class="sidebar-brand-title">Sistema de Apoyo</div>
            <div class="sidebar-brand-subtitle">Salud mental y autogestión</div>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=[
                "Datos informativos",
                "Estadísticas",
                "Evaluaciones",
                "Historial",
                "Seguimiento emocional",
                "Recomendaciones",
                "Progreso y reportes",
                "Configuración",
                "Cerrar sesión"
            ],
            icons=[
                "info-circle",
                "bar-chart-line",
                "clipboard2-pulse",
                "clock-history",
                "emoji-smile",
                "lightbulb",
                "gear",
                "box-arrow-right"
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#4A90E2",
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "17px",
                    "text-align": "left",
                    "margin": "8px 0",
                    "padding": "12px 14px",
                    "border-radius": "12px",
                    "color": "#1f2937",
                    "--hover-color": "#eef4ff"
                },
                "nav-link-selected": {
                    "background-color": "#4A90E2",
                    "color": "white",
                    "font-weight": "600"
                }
            }
        )

    return selected