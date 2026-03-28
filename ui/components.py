import streamlit as st


def render_section_header(title, icon="📋"):
    st.markdown(f"""
    <div class="section-header">
        <span class="section-header-icon">{icon}</span>
        <h3 class="section-title" style="margin: 0;">{title}</h3>
    </div>
    """, unsafe_allow_html=True)


def render_card(title=None, icon=None):
    container = st.container()
    with container:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if title:
            st.markdown(f"""
            <div class="card-header">
                <h4 class="card-title">{" ".join(filter(None, [icon, title]))}</h4>
            </div>
            """, unsafe_allow_html=True)
    return container


def end_card():
    st.markdown('</div>', unsafe_allow_html=True)


def render_metric_card(label, value, delta=None, icon=None, help_text=None):
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        if icon:
            st.markdown(f"<div style='font-size: 1.5rem;'>{icon}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='width: 24px;'></div>", unsafe_allow_html=True)
    with col2:
        st.metric(label=label, value=value, delta=delta, help=help_text)


def render_badge(text, type="primary"):
    badge_class = f"badge badge-{type}"
    st.markdown(f'<span class="{badge_class}">{text}</span>', unsafe_allow_html=True)


def render_info_box(text):
    st.markdown(f"""
    <div class="info-box">
        {text}
    </div>
    """, unsafe_allow_html=True)


def render_warning_box(text):
    st.markdown(f"""
    <div class="warning-box">
        {text}
    </div>
    """, unsafe_allow_html=True)


def render_success_box(text):
    st.markdown(f"""
    <div class="success-box">
        {text}
    </div>
    """, unsafe_allow_html=True)


def render_accordion(items, default_open=None):
    for i, (title, content) in enumerate(items):
        with st.expander(f"{'📂 ' if default_open == i else '📁 '} {title}", expanded=(default_open == i)):
            st.markdown(content)


def render_result_badge(nivel):
    if "Severa" in nivel or "Alto" in nivel or "Riesgo" in nivel:
        return "danger", "🔴"
    elif "Moderada" in nivel or "Medio" in nivel:
        return "warning", "🟡"
    else:
        return "success", "🟢"


def render_quick_stats(total, realizadas, no_realizadas, porcentaje):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("Realizadas", realizadas)
    with col3:
        st.metric("Pendientes", no_realizadas)
    with col4:
        st.metric("Cumplimiento", f"{porcentaje}%")


def render_page_header(title, subtitle=None, icon=None):
    st.markdown(f"""
    <div class="welcome-banner">
        <h2>{" ".join(filter(None, [icon, title]))}</h2>
        {f'<p style="color: var(--text-secondary); margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_divider_with_text(text):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='text-align: center; color: var(--text-secondary); font-size: 0.85rem; margin: 0;'>{text}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)


def render_action_buttons(primary_label, secondary_label=None, key_prefix=""):
    col1, col2 = st.columns([1, 1] if secondary_label else [1])
    
    with col1:
        st.button(primary_label, type="primary", use_container_width=True, key=f"{key_prefix}_primary")
    
    if secondary_label:
        with col2:
            st.button(secondary_label, use_container_width=True, key=f"{key_prefix}_secondary")


def render_empty_state(icon, title, description):
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">{title}</h3>
        <p style="color: var(--text-secondary);">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(value, max_value, label=None, color="primary"):
    if label:
        st.caption(f"{label}: {value}/{max_value}")
    st.progress(value / max_value if max_value > 0 else 0)
