import streamlit as st


def load_styles():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0.6rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: #374151;
        margin-bottom: 1.5rem;
    }

    .hero-section {
        max-width: 1000px;
        margin: 1.5rem auto 1rem auto;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        background: #e8f1ff;
        color: #2d5ea8;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .hero-text {
        color: #4b5563;
        font-size: 1.08rem;
        max-width: 850px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.8;
    }

    .form-card {
        background: white;
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
        max-width: 900px;
        margin: auto;
    }

    .mini-card {
        background: white;
        padding: 1.2rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        max-width: 900px;
        margin: auto;
    }

    .sidebar-user-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background: white;
        padding: 14px;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        margin-bottom: 14px;
    }

    .sidebar-user-icon {
        font-size: 1.6rem;
    }

    .sidebar-user-label {
        font-size: 0.8rem;
        color: #6b7280;
    }

    .sidebar-user-name {
        font-size: 1rem;
        font-weight: 700;
        color: #1f2937;
    }

    .sidebar-brand-card {
        background: linear-gradient(135deg, #4A90E2 0%, #6aa8ee 100%);
        padding: 18px;
        border-radius: 18px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 10px 24px rgba(74,144,226,0.25);
    }

    .sidebar-brand-title {
        font-size: 1.15rem;
        font-weight: 800;
    }

    .sidebar-brand-subtitle {
        font-size: 0.9rem;
        opacity: 0.95;
        margin-top: 4px;
    }

    .content-header {
        background: white;
        border-radius: 20px;
        padding: 24px 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }

    .content-header h1 {
        color: #1f2937;
        margin-bottom: 8px;
    }

    .content-header p {
        color: #4b5563;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
    }

    .content-badge {
        display: inline-block;
        background: #eef4ff;
        color: #2d5ea8;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .stButton > button {
        background: #4A90E2;
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: none;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #357ABD;
        color: white;
    }

    .recommendation-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    margin-bottom: 18px;
    border-left: 6px solid #4A90E2;
    }

    .recommendation-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 10px;
    }

    .recommendation-section {
        margin-top: 10px;
        margin-bottom: 10px;
        color: #374151;
        line-height: 1.7;
    }

    .recommendation-label {
        font-weight: 700;
        color: #2d5ea8;
    }

    .recommendation-empty {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        padding: 24px;
        border-radius: 18px;
        text-align: center;
        color: #475569;
    }                       
                
    </style>
    """, unsafe_allow_html=True)