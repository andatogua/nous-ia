import streamlit as st
from ui.styles import load_styles

st.set_page_config(
    page_title="Términos y Condiciones",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()

st.title("Términos y Condiciones")
st.subheader("Información educativa y legal")

st.markdown("""
### 1. Finalidad del sistema
Esta plataforma es un sistema web de apoyo educativo para la detección y autogestión de síntomas de depresión.
No reemplaza el diagnóstico psicológico o psiquiátrico profesional.

### 2. Uso responsable
El usuario se compromete a utilizar el sistema de manera honesta y responsable, proporcionando información veraz
en los cuestionarios y registros de seguimiento.

### 3. Protección de datos personales
La información del usuario debe ser tratada con confidencialidad, respetando la privacidad y los principios de
protección de datos personales.

### 4. Consentimiento informado
Al registrarse, el usuario reconoce que:
- el sistema tiene un carácter educativo y de apoyo,
- los resultados son orientativos y no constituyen un diagnóstico clínico definitivo,
- algunas recomendaciones pueden ser generadas automáticamente.

### 5. Relación con legislación informática
Este sistema se vincula con principios de legislación informática, tales como:
- protección de la privacidad,
- tratamiento responsable de la información digital,
- consentimiento informado,
- uso ético de herramientas tecnológicas en contextos relacionados con salud.

### 6. Limitación de responsabilidad
Los desarrolladores y el equipo académico no se responsabilizan por decisiones tomadas exclusivamente con base
en resultados automáticos del sistema. En casos de síntomas severos o riesgo, se recomienda buscar ayuda profesional inmediata.
""")

if st.button("Volver al registro", use_container_width=True):
    st.switch_page("pages/register.py")