import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar(user_name: str):
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">NousIA</div>
            <div class="sidebar-brand-subtitle">Sistema de Apoyo Emocional</div>
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
                    <div class="sidebar-user-label">Usuario conectado</div>
                    <div class="sidebar-user-name">{user_name}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        menu_options = [
            "Datos informativos",
            "Estadísticas",
            "Evaluaciones",
            "Recomendaciones",
            "Seguimiento emocional",
            "Historial",
            "Configuración",
            "Cerrar sesión"
        ]

        menu_icons = [
            "house-door",
            "bar-chart-line",
            "clipboard2-pulse",
            "lightbulb",
            "emoji-smile",
            "clock-history",
            "gear",
            "box-arrow-right"
        ]

        current_page = st.session_state.get("current_page", "Datos informativos")
        default_index = menu_options.index(current_page) if current_page in menu_options else 0
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=menu_icons,
            default_index=default_index,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                    "margin-top": "6px"
                },
                "icon": {
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "3px 0",
                    "padding": "10px 14px",
                    "border-radius": "10px",
                    "color": "#1F2937",
                    "font-weight": "500",
                    "--hover-color": "#F0FDFA"
                },
                "nav-link-selected": {
                    "background-color": "#52b44a",
                    "color": "white",
                    "font-weight": "600",
                    "border-radius": "10px"
                },
                "nav-link:hover": {
                    "background-color": "#F0FDFA"
                }
            },
            key="main_menu"
        )

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #9CA3AF; font-size: 0.75rem;">
            <p style="margin: 0;">NousIA v1.0</p>
            <p style="margin: 4px 0 0 0;">Sistema de Apoyo Educativo</p>
        </div>
        """, unsafe_allow_html=True)

    return selected
