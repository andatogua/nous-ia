import streamlit as st
from services.auth_service import AuthService
from ui.styles import load_styles
from utils.session_manager import initialize_session
from datetime import date, timedelta

st.set_page_config(
    page_title="NousIA - Iniciar sesión",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()
initialize_session()

if st.session_state.user:
    st.switch_page("pages/dashboard.py")

sex_options = {
    "Masculino": 1,
    "Femenino": 2,
    "Otro": 3,
    "Prefiero no decirlo": 4
}

today = date.today()
max_birth_date = today - timedelta(days=18 * 365)
min_birth_date = today - timedelta(days=50 * 365)

register_defaults = {
    "reg_cedula": "",
    "reg_nombre": "",
    "reg_apellido": "",
    "reg_correo": "",
    "reg_telefono": "",
    "reg_fecha_nacimiento": None,
    "reg_sexo": None,
    "reg_username": "",
    "reg_password": "",
    "reg_confirm_password": "",
    "reg_accept_terms": False,
    "clear_register_form": False,
    "register_success": False
}

for key, value in register_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.clear_register_form:
    st.session_state.reg_cedula = ""
    st.session_state.reg_nombre = ""
    st.session_state.reg_apellido = ""
    st.session_state.reg_correo = ""
    st.session_state.reg_telefono = ""
    st.session_state.reg_fecha_nacimiento = None
    st.session_state.reg_sexo = None
    st.session_state.reg_username = ""
    st.session_state.reg_password = ""
    st.session_state.reg_confirm_password = ""
    st.session_state.reg_accept_terms = False
    st.session_state.clear_register_form = False


@st.dialog("Términos y Condiciones")
def show_terms_dialog():
    st.markdown("""
    <div style="padding: 1rem;">
        <h3 style="color: #52b44a; margin-bottom: 1rem;">📜 Términos y Condiciones</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 1. Finalidad del sistema
    NousIA es una plataforma de apoyo educativo orientada a la detección inicial, autogestión y seguimiento de síntomas emocionales. No reemplaza la atención profesional en salud mental.

    ### 2. Uso responsable
    El usuario se compromete a utilizar el sistema de forma honesta, responsable y proporcionando información veraz en los cuestionarios y registros.

    ### 3. Privacidad y consentimiento
    La información registrada será tratada con confidencialidad. Al utilizar la plataforma, el usuario comprende que los resultados son orientativos y no constituyen un diagnóstico clínico.

    ### 4. Limitación de responsabilidad
    Si existen síntomas severos, malestar persistente o situaciones de riesgo, se recomienda acudir a un profesional de salud mental.
    """)
    
    st.markdown("""
    <div style="background-color: #FEF3C7; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <strong>⚠️ Nota importante:</strong> El uso de la plataforma implica la aceptación de estas condiciones.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Cerrar", use_container_width=True):
        st.rerun()


col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    <style>
    .left-panel {
        background: linear-gradient(135deg, #52b44a 0%, #467c42 50%, #001f3d 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        color: white;
    }
    .left-panel h1 {
        color: white !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin: 0 0 1rem 0 !important;
    }
    .left-panel .tagline {
        color: rgba(255,255,255,0.9);
        font-size: 1.15rem;
        max-width: 320px;
        line-height: 1.6;
        margin: 0;
    }
    .left-panel .features {
        display: flex;
        gap: 2rem;
        margin-top: 3rem;
    }
    .left-panel .feature {
        text-align: center;
    }
    .left-panel .feature-icon {
        font-size: 2.5rem;
    }
    .left-panel .feature-text {
        color: white;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .left-panel .footer {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.2);
        max-width: 320px;
    }
    .left-panel .footer p {
        color: rgba(255,255,255,0.7);
        font-size: 0.8rem;
        margin: 0;
    }
    </style>
    
    <div class="left-panel">
        <h1>NousIA</h1>
        <p class="tagline">Tu compañero digital para el bienestar emocional. Evalúa, aprende y mejora tu salud mental.</p>
        <div class="features">
            <div class="feature">
                <div class="feature-icon">📊</div>
                <p class="feature-text">Evaluaciones</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <p class="feature-text">Recomendaciones</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📈</div>
                <p class="feature-text">Seguimiento</p>
            </div>
        </div>
        <div class="footer">
            <p>Sistema de apoyo educativo basado en guías clínicas internacionales (NICE NG222)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='padding: 1rem;'></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Iniciar sesión", "📝 Registrarse"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image("assets/logo_nousia_banner.png", width=600)
        
        with st.form("login_form", clear_on_submit=False):
            correo = st.text_input(
                "Correo electrónico",
                placeholder="ejemplo@correo.com",
                key="login_correo"
            )
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingrese su contraseña",
                key="login_password"
            )
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Iniciar sesión", use_container_width=True)
            
            if submit:
                if not correo.strip() or not password.strip():
                    st.warning("Por favor, complete todos los campos.")
                else:
                    with st.spinner("Verificando credenciales..."):
                        success, message, user = AuthService.login_user(correo, password)
                    
                    if success:
                        st.session_state.user = user
                        st.success("¡Inicio de sesión exitoso!")
                        if user.get("ID_ROL") == 3:
                            st.switch_page("pages/specialist.py")
                        else:
                            st.switch_page("pages/dashboard.py")
                    else:
                        st.error("Correo o contraseña incorrectos.")
    
    with tab2:      
        st.markdown("""
        <div style="
            background-color: #EFF6FF;
            border-left: 4px solid #3B82F6;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        ">
            Antes de registrarse, lea los <strong>términos y condiciones</strong> del sistema.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Leer términos y condiciones", type="secondary", use_container_width=True):
            show_terms_dialog()
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                cedula = st.text_input("Cédula *", placeholder="V-12345678")
            
            with col2:
                nombre = st.text_input("Nombre *", placeholder="María")
            
            col3, col4 = st.columns(2)
            
            with col3:
                apellido = st.text_input("Apellido *", placeholder="García")
            
            with col4:
                telefono = st.text_input("Teléfono", placeholder="0412-1234567")
            
            correo_registro = st.text_input("Correo electrónico *", placeholder="ejemplo@correo.com")
            
            col5, col6 = st.columns(2)
            
            with col5:
                fecha_nacimiento = st.date_input(
                    "Fecha de nacimiento *",
                    value=st.session_state.reg_fecha_nacimiento,
                    min_value=min_birth_date,
                    max_value=max_birth_date
                )
            
            with col6:
                sexo = st.selectbox(
                    "Sexo *",
                    list(sex_options.keys()),
                    key="reg_sexo",
                    index=None,
                    placeholder="Seleccione"
                )
            
            username = st.text_input("Nombre de usuario *", placeholder="usuario123")
            
            col7, col8 = st.columns(2)
            
            with col7:
                password_registro = st.text_input("Contraseña *", type="password", placeholder="Mínimo 8 caracteres")
            
            with col8:
                confirm_password = st.text_input("Confirmar contraseña *", type="password", placeholder="Repita la contraseña")
            
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            
            accept_terms = st.checkbox(
                "Acepto los términos y condiciones del sistema",
                key="reg_accept_terms"
            )
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            submit_register = st.form_submit_button("Crear cuenta", use_container_width=True)
            
            if submit_register:
                st.session_state.register_success = False
                
                if (
                    not cedula.strip()
                    or not nombre.strip()
                    or not apellido.strip()
                    or not correo_registro.strip()
                    or not username.strip()
                    or not password_registro.strip()
                    or not confirm_password.strip()
                ):
                    st.warning("Por favor, complete todos los campos obligatorios (*).")
                elif not fecha_nacimiento:
                    st.warning("Por favor, seleccione su fecha de nacimiento.")
                elif sexo is None:
                    st.warning("Por favor, seleccione su sexo.")
                else:
                    edad = today.year - fecha_nacimiento.year - (
                        (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
                    )
                    
                    if password_registro != confirm_password:
                        st.warning("Las contraseñas no coinciden.")
                    elif len(password_registro) < 8:
                        st.warning("La contraseña debe tener al menos 8 caracteres.")
                    elif edad < 18 or edad > 50:
                        st.warning("La edad permitida para registrarse es de 18 a 50 años.")
                    elif not accept_terms:
                        st.warning("Debe aceptar los términos y condiciones para continuar.")
                    else:
                        user_data = {
                            "cedula": cedula,
                            "nombre": nombre,
                            "apellido": apellido,
                            "correo": correo_registro,
                            "telefono": telefono,
                            "fecha_nacimiento": fecha_nacimiento,
                            "id_sexo": sex_options[sexo],
                            "username": username,
                            "password": password_registro,
                            "id_rol": 1
                        }
                        
                        with st.spinner("Registrando usuario..."):
                            success, message = AuthService.register_user(user_data)
                        
                        if success:
                            st.session_state.clear_register_form = True
                            st.session_state.register_success = True
                            st.rerun()
                        else:
                            st.error(message)
        
        if st.session_state.register_success:
            st.success("✅ Cuenta creada exitosamente. Ya puede iniciar sesión con sus credenciales.")
            st.session_state.register_success = False
