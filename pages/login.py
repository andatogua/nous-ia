import streamlit as st 
from services.auth_service import AuthService
from ui.styles import load_styles
from utils.session_manager import initialize_session


st.set_page_config(
    page_title="Iniciar sesión - Sistema de Apoyo para la Salud Mental",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()
initialize_session()

# Si ya hay sesión activa, ir directo al panel principal
if st.session_state.user:
    st.switch_page("pages/dashboard.py")

st.markdown("""
<div class="hero-section">
    <div class="hero-badge">Salud mental • Apoyo educativo • Evaluación inicial</div>
    <h1 class="main-title">🧠 Sistema Web de Apoyo para la Salud Mental</h1>
    <p class="hero-text">
        Plataforma orientada a la detección inicial, autogestión y seguimiento de síntomas depresivos,
        mediante herramientas educativas y cuestionarios como PHQ-9 y WHO-5.
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Iniciar sesión", "Registrarse"])

with tab1:
    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
    st.subheader("Acceso al sistema")

    with st.form("login_form"):
        correo = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar", use_container_width=True)

    if submit:
        if not correo.strip() or not password.strip():
            st.warning("Por favor, complete todos los campos.")
        else:
            with st.spinner("Verificando credenciales..."):
                success, message, user = AuthService.login_user(correo, password)

            if success:
                st.session_state.user = user
                st.success("Inicio de sesión exitoso. Redirigiendo...")
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Correo o contraseña incorrectos.")

    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
    st.info("Si aún no tienes cuenta, regístrate para acceder al sistema.")
    if st.button("Ir a registro", use_container_width=True):
        st.switch_page("pages/register.py")
    st.markdown("</div>", unsafe_allow_html=True)