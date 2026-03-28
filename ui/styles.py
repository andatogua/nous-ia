import streamlit as st


def load_styles():
    st.markdown("""
    <style>
    :root {
        --primary: #52b44a;
        --primary-dark: #467c42;
        --primary-light: #75ca6e;
        --accent: #001f3d;
        --bg-main: #F8FAFB;
        --bg-card: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --text-muted: #9CA3AF;
        --border: #E5E7EB;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --radius: 12px;
        --radius-lg: 16px;
    }

    /* ============ BASE ============ */
    .stApp {
        background-color: var(--bg-main);
    }

    /* ============ TYPOGRAPHY ============ */
    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-weight: 700;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }

    .subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
    }

    /* ============ BUTTONS ============ */
    .stButton > button {
        border-radius: var(--radius);
        font-weight: 600;
        padding: 0.65rem 1.25rem;
        border: none;
        transition: all 0.2s ease;
    }

    .stButton > button.primary {
        background-color: var(--primary);
        color: white;
    }

    .stButton > button.primary:hover {
        background-color: var(--primary-dark);
        color: white;
    }

    /* Form submit buttons */
    .stFormSubmitButton > button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: var(--radius) !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    .stFormSubmitButton > button:hover {
        background-color: var(--primary-dark) !important;
        color: white !important;
    }

    .stFormSubmitButton > button:focus {
        background-color: var(--primary-dark) !important;
    }

    /* Secondary buttons */
    button[kind="secondary"] {
        background: none !important;
        border: none !important;
        color: var(--primary) !important;
        padding: 0 !important;
    }

    button[kind="secondary"]:hover {
        color: var(--primary-dark) !important;
    }

    /* ============ INPUTS ============ */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.65rem 0.875rem;
        color: var(--text-primary);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15);
        outline: none;
    }

    .stTextInput > div > label,
    .stNumberInput > div > label,
    .stDateInput > div > label,
    .stTextArea > div > label,
    .stSelectbox > div > label {
        color: var(--text-secondary);
        font-weight: 500;
        margin-bottom: 0.35rem;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: transparent;
    }

    .stRadio label {
        color: var(--text-primary);
    }

    /* Checkbox */
    .stCheckbox > label {
        color: var(--text-secondary);
    }

    /* ============ TABS ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid var(--border);
        padding-bottom: 0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius) var(--radius) 0 0;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        color: var(--text-secondary);
        background-color: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        margin-bottom: -2px;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary);
        background-color: rgba(13, 148, 136, 0.05);
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
        background-color: transparent !important;
    }

    /* ============ CARDS ============ */
    .card {
        background-color: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
    }

    .card-header {
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    /* ============ METRICS ============ */
    [data-testid="stMetric"] {
        background-color: var(--bg-card);
        border-radius: var(--radius);
        padding: 1rem;
        border: 1px solid var(--border);
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-weight: 700;
        font-size: 1.5rem;
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1rem;
    }

    .sidebar-brand {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-md);
    }

    .sidebar-brand-title {
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .sidebar-brand-subtitle {
        font-size: 0.85rem;
        opacity: 0.9;
    }

    .sidebar-user-card {
        background: linear-gradient(135deg, #f0fdfa 0%, #ecfdf5 100%);
        border: 1px solid rgba(13, 148, 136, 0.2);
        border-radius: var(--radius-lg);
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-user-icon {
        width: 40px;
        height: 40px;
        background-color: var(--primary);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.1rem;
    }

    .sidebar-user-name {
        font-weight: 700;
        color: var(--text-primary);
        font-size: 0.95rem;
    }

    .sidebar-user-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    /* Nav menu */
    .sidebar-nav {
        margin-top: 0.5rem;
    }

    /* ============ ALERTS & MESSAGES ============ */
    .stAlert {
        border-radius: var(--radius);
        border: none;
    }

    /* Success */
    div[data-testid="stAlert"]:has([data-testid="stAlertSuccess"]) {
        background-color: #ecfdf5;
        border-left: 4px solid var(--success);
    }

    /* Warning */
    div[data-testid="stAlert"]:has([data-testid="stAlertWarning"]) {
        background-color: #fffbeb;
        border-left: 4px solid var(--warning);
    }

    /* Error */
    div[data-testid="stAlert"]:has([data-testid="stAlertError"]) {
        background-color: #fef2f2;
        border-left: 4px solid var(--danger);
    }

    /* Info */
    div[data-testid="stAlert"]:has([data-testid="stAlertInfo"]) {
        background-color: #eff6ff;
        border-left: 4px solid #3B82F6;
    }

    /* ============ DIVIDER ============ */
    hr {
        border: none;
        height: 1px;
        background-color: var(--border);
        margin: 1.5rem 0;
    }

    /* ============ TABLES ============ */
    .stDataFrame {
        border-radius: var(--radius);
        overflow: hidden;
    }

    /* ============ SPINNER ============ */
    .stSpinner > div {
        border-color: var(--primary);
    }

    /* ============ PROGRESS ============ */
    .stProgress > div > div {
        background-color: var(--primary);
    }

    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        background-color: var(--bg-card);
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }

    /* ============ BADGES ============ */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-success {
        background-color: #ecfdf5;
        color: var(--success);
    }

    .badge-warning {
        background-color: #fffbeb;
        color: var(--warning);
    }

    .badge-danger {
        background-color: #fef2f2;
        color: var(--danger);
    }

    .badge-info {
        background-color: #eff6ff;
        color: #3B82F6;
    }

    .badge-primary {
        background-color: rgba(13, 148, 136, 0.1);
        color: var(--primary);
    }

    /* ============ MINI CARDS (Dashboard info cards) ============ */
    .mini-card {
        background-color: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }

    .mini-card h4 {
        color: var(--primary);
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    /* ============ SECTION HEADER ============ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .section-header::after {
        content: "";
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, var(--primary) 0%, transparent 100%);
        opacity: 0.3;
    }

    .section-header-icon {
        color: var(--primary);
    }

    /* ============ LOGIN PAGE SPECIFIC ============ */
    /* Full page layout using injected HTML */
    .login-page-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        margin: 0 !important;
        padding: 0 !important;
    }

    .login-left-panel {
        flex: 1.1;
        background: linear-gradient(135deg, #52b44a 0%, #467c42 50%, #001f3d 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
    }

    .login-left-panel h1 {
        color: white !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin: 1rem 0 !important;
    }

    .login-left-panel .tagline {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        max-width: 320px;
        line-height: 1.6;
    }

    .login-left-panel .features {
        display: flex;
        gap: 2rem;
        margin-top: 2rem;
    }

    .login-left-panel .feature-item {
        text-align: center;
    }

    .login-left-panel .feature-icon {
        font-size: 2rem;
    }

    .login-left-panel .feature-text {
        color: white;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    .login-left-panel .footer-note {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.2);
        max-width: 320px;
    }

    .login-left-panel .footer-note p {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.8rem !important;
    }

    .login-right-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        background-color: var(--bg-main);
    }

    .login-form-container {
        background-color: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 2rem;
        width: 100%;
        max-width: 440px;
        box-shadow: var(--shadow-lg);
    }

    /* ============ FORM STYLING ============ */
    .form-group {
        margin-bottom: 1rem;
    }

    .form-row {
        display: flex;
        gap: 1rem;
    }

    .form-row > div {
        flex: 1;
    }

    /* ============ RESULTS CARDS ============ */
    .result-card {
        background-color: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }

    .result-card-high {
        border-left: 4px solid var(--danger);
    }

    .result-card-medium {
        border-left: 4px solid var(--warning);
    }

    .result-card-low {
        border-left: 4px solid var(--success);
    }

    /* ============ CUSTOM SCROLLBAR ============ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* ============ RESPONSIVE ============ */
    @media (max-width: 768px) {
        .login-left {
            display: none;
        }
        
        .login-right {
            flex: 1;
        }
        
        .login-card {
            max-width: 100%;
        }
    }

    /* ============ WELCOME BANNER ============ */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%);
        border: 1px solid rgba(13, 148, 136, 0.2);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .welcome-banner h2 {
        color: var(--primary);
        margin-bottom: 0.5rem;
    }

    /* ============ ACCENT LINE ============ */
    .accent-line {
        width: 60px;
        height: 4px;
        background-color: var(--primary);
        border-radius: 2px;
        margin-bottom: 1rem;
    }

    /* ============ INFO BOX ============ */
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3B82F6;
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .warning-box {
        background-color: #fffbeb;
        border-left: 4px solid var(--warning);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .success-box {
        background-color: #ecfdf5;
        border-left: 4px solid var(--success);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
