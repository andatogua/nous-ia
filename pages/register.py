import streamlit as st
from services.auth_service import AuthService
from ui.styles import load_styles
from utils.session_manager import initialize_session


st.set_page_config(
    page_title="Registro - Sistema de Apoyo para la Salud Mental",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()
initialize_session()

sex_options = {
    "Masculino": 1,
    "Femenino": 2,
    "Otro": 3,
    "Prefiero no decirlo": 4
}

st.markdown("""
<div class="hero-section">
    <div class="hero-badge">Registro de usuario</div>
    <h1 class="main-title">🧠 Crear cuenta</h1>
    <p class="hero-text">
        Complete sus datos para acceder al sistema. La información será utilizada
        únicamente dentro del entorno del proyecto.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='form-card'>", unsafe_allow_html=True)

with st.form("register_form"):
    cedula = st.text_input("Cédula")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Teléfono")
    fecha_nacimiento = st.date_input("Fecha de nacimiento")
    sexo = st.selectbox("Sexo", list(sex_options.keys()))
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar contraseña", type="password")

    st.markdown("Debe leer y aceptar los términos y condiciones antes de registrarse.")

    accept_terms = st.checkbox("Acepto los términos y condiciones")

    submit = st.form_submit_button("Crear cuenta", use_container_width=True)

if st.button("Leer términos y condiciones", use_container_width=True):
    st.switch_page("pages/terms_and_conditions.py")

if submit:
    if (
        not cedula.strip() or
        not nombre.strip() or
        not apellido.strip() or
        not correo.strip() or
        not telefono.strip() or
        not username.strip() or
        not password.strip() or
        not confirm_password.strip()
    ):
        st.warning("Por favor, complete todos los campos.")

    elif password != confirm_password:
        st.warning("Las contraseñas no coinciden.")

    elif not accept_terms:
        st.warning("Debe aceptar los términos y condiciones para continuar.")

    else:
        user_data = {
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "telefono": telefono,
            "fecha_nacimiento": fecha_nacimiento,
            "id_sexo": sex_options[sexo],
            "username": username,
            "password": password,
            "id_rol": 1
        }

        with st.spinner("Registrando usuario..."):
            success, message = AuthService.register_user(user_data)

        if success:
            st.success("Usuario registrado correctamente.")
            st.info("Ahora puede iniciar sesión.")
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Volver a iniciar sesión", use_container_width=True):
    st.switch_page("pages/login.py")