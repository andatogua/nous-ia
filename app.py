import streamlit as st
from ui.styles import load_styles
from utils.session_manager import initialize_session
from database.init_database import DatabaseInitializer


def main():
    st.set_page_config(
        page_title="Sistema Web de Apoyo para la Salud Mental",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    print(st.session_state)
    if 'db_initialized' not in st.session_state:
        DatabaseInitializer.initialize()
        st.session_state.db_initialized = True

    load_styles()
    initialize_session()

    if st.session_state.user:
        st.switch_page("pages/dashboard.py")
    else:
        st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()