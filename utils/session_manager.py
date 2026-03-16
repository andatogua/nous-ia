import streamlit as st


def initialize_session():

    if "user" not in st.session_state:
        st.session_state.user = None

    if "screen" not in st.session_state:
        st.session_state.screen = "login"


def logout():

    st.session_state.user = None
    st.session_state.screen = "login"