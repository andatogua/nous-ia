import streamlit as st
from services.auth_service import AuthService
from ui.styles import load_styles
from utils.session_manager import initialize_session

st.set_page_config(
    page_title="Registro - NousIA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()
initialize_session()

st.markdown("""
<div style="
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #52b44a 0%, #467c42 100%);
    color: white;
    margin: -1rem -1rem 2rem -1rem;
">
    <h1 style="margin: 0; font-size: 2rem;">Crear cuenta</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Complete sus datos para acceder al sistema</p>
</div>
""", unsafe_allow_html=True)

sex_options = {
    "Masculino": 1,
    "Femenino": 2,
    "Otro": 3,
    "Prefiero no decirlo": 4
}

st.markdown("""
<div style="
    background-color: #EFF6FF;
    border-left: 4px solid #3B82F6;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
">
    <strong>📋 Información:</strong> Antes de registrarse, lea los términos y condiciones del sistema.
</div>
""", unsafe_allow_html=True)

with st.expander("📄 Leer términos y condiciones"):
    st.markdown("""
    ### 1. Finalidad del sistema
    NousIA es una plataforma de apoyo educativo para la detección y autogestión de síntomas de depresión. No reemplaza el diagnóstico profesional.

    ### 2. Uso responsable
    El usuario se compromete a utilizar el sistema de manera honesta, proporcionando información veraz en los cuestionarios.

    ### 3. Protección de datos
    La información del usuario será tratada con confidencialidad y respeto a la privacidad.

    ### 4. Limitación de responsabilidad
    En casos de síntomas severos o riesgo, se recomienda buscar ayuda profesional.
    """)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

with st.form("register_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        cedula = st.text_input("Cédula *", placeholder="V-12345678")
        nombre = st.text_input("Nombre *", placeholder="María")
        telefono = st.text_input("Teléfono", placeholder="0412-1234567")
    
    with col2:
        apellido = st.text_input("Apellido *", placeholder="García")
        correo = st.text_input("Correo electrónico *", placeholder="correo@ejemplo.com")
        username = st.text_input("Nombre de usuario *", placeholder="usuario123")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fecha_nacimiento = st.date_input("Fecha de nacimiento *")
    
    with col4:
        sexo = st.selectbox("Sexo *", list(sex_options.keys()), index=None, placeholder="Seleccione")
    
    col5, col6 = st.columns(2)
    
    with col5:
        password = st.text_input("Contraseña *", type="password")
    
    with col6:
        confirm_password = st.text_input("Confirmar contraseña *", type="password")
    
    accept_terms = st.checkbox("Acepto los términos y condiciones *")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    submit = st.form_submit_button("Crear cuenta", use_container_width=True)

if submit:
    if (
        not cedula.strip() or
        not nombre.strip() or
        not apellido.strip() or
        not correo.strip() or
        not username.strip() or
        not password.strip() or
        not confirm_password.strip()
    ):
        st.warning("Por favor, complete todos los campos obligatorios (*).")
    elif not fecha_nacimiento:
        st.warning("Por favor, seleccione su fecha de nacimiento.")
    elif sexo is None:
        st.warning("Por favor, seleccione su sexo.")
    elif password != confirm_password:
        st.warning("Las contraseñas no coinciden.")
    elif len(password) < 8:
        st.warning("La contraseña debe tener al menos 8 caracteres.")
    elif not accept_terms:
        st.warning("Debe aceptar los términos y condiciones.")
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
            "id_rol": 2 #ROL DE PACIENTE
        }
        
        with st.spinner("Registrando usuario..."):
            success, message = AuthService.register_user(user_data)
        
        if success:
            st.success("✅ Usuario registrado correctamente. Ahora puede iniciar sesión.")
        else:
            st.error(message)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("← Volver a iniciar sesión", use_container_width=True):
        st.switch_page("pages/login.py")
