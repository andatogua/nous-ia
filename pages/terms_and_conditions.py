import streamlit as st
from ui.styles import load_styles

st.set_page_config(
    page_title="Términos y Condiciones - NousIA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()

st.markdown("""
<div style="
    background: linear-gradient(135deg, #52b44a 0%, #467c42 100%);
    padding: 2rem;
    margin: -1rem -1rem 2rem -1rem;
    color: white;
    text-align: center;
">
    <h1 style="margin: 0; font-size: 2rem;">Términos y Condiciones</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Información educativa y legal del sistema</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card" style="margin-bottom: 1rem;">
    <h4 style="color: #52b44a; margin-bottom: 0.75rem;">1. Finalidad del sistema</h4>
    <p style="color: #4B5563; margin: 0;">
        Esta plataforma es un sistema web de apoyo educativo para la detección y autogestión de síntomas de depresión. 
        No reemplaza el diagnóstico psicológico o psiquiátrico profesional.
    </p>
</div>

<div class="card" style="margin-bottom: 1rem;">
    <h4 style="color: #52b44a; margin-bottom: 0.75rem;">2. Uso responsable</h4>
    <p style="color: #4B5563; margin: 0;">
        El usuario se compromete a utilizar el sistema de manera honesta y responsable, proporcionando información veraz 
        en los cuestionarios y registros de seguimiento.
    </p>
</div>

<div class="card" style="margin-bottom: 1rem;">
    <h4 style="color: #52b44a; margin-bottom: 0.75rem;">3. Protección de datos personales</h4>
    <p style="color: #4B5563; margin: 0;">
        La información del usuario debe ser tratada con confidencialidad, respetando la privacidad y los principios de 
        protección de datos personales.
    </p>
</div>

<div class="card" style="margin-bottom: 1rem;">
    <h4 style="color: #52b44a; margin-bottom: 0.75rem;">4. Consentimiento informado</h4>
    <p style="color: #4B5563; margin: 0;">
        Al registrarse, el usuario reconoce que:
    </p>
    <ul style="color: #4B5563;">
        <li>El sistema tiene un carácter educativo y de apoyo.</li>
        <li>Los resultados son orientativos y no constituyen un diagnóstico clínico.</li>
        <li>Algunas recomendaciones pueden ser generadas automáticamente.</li>
    </ul>
</div>

<div class="card" style="margin-bottom: 1rem;">
    <h4 style="color: #52b44a; margin-bottom: 0.75rem;">5. Limitación de responsabilidad</h4>
    <p style="color: #4B5563; margin: 0;">
        Los desarrolladores no se responsabilizan por decisiones tomadas exclusivamente con base en resultados 
        automáticos del sistema. En casos de síntomas severos o riesgo, se recomienda buscar ayuda profesional inmediata.
    </p>
</div>

<div style="
    background-color: #FEF3C7;
    border-left: 4px solid #F59E0B;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 1.5rem;
">
    <strong>⚠️ Aviso importante:</strong> Si experimenta pensamientos de autolesión o crisis, por favor contacte a un profesional de salud mental o líneas de crisis disponibles en su país.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("← Volver al login", use_container_width=True):
        st.switch_page("pages/login.py")
