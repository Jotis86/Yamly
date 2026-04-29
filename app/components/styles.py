"""Global CSS styles injected into the Streamlit app."""

import streamlit as st


def inject_global_styles() -> None:
    """Inject custom CSS for the GitHub Actions Hub app."""
    st.markdown(
        """
        <style>
        /* ── Fonts & base ─────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ── Hide default Streamlit chrome ────────────────────────── */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { display: none; }

        /* ── App background ────────────────────────────────────────── */
        .stApp {
            background: #0d1117;
        }

        /* ── Sidebar ───────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #c9d1d9 !important;
        }

        /* ── Hero banner ───────────────────────────────────────────── */
        .hero-banner {
            background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 50%, #0d1117 100%);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 48px 40px;
            text-align: center;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at center, rgba(88,166,255,0.08) 0%, transparent 60%);
            pointer-events: none;
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: #f0f6fc;
            margin: 0 0 12px 0;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            color: #8b949e;
            margin: 0 0 24px 0;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(88,166,255,0.15);
            color: #58a6ff;
            border: 1px solid rgba(88,166,255,0.3);
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 0.85rem;
            font-weight: 500;
            margin: 4px;
        }

        /* ── Template card ─────────────────────────────────────────── */
        .template-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .template-card:hover {
            border-color: #58a6ff;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(88,166,255,0.15);
        }
        .template-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #58a6ff, #bc8cff);
            opacity: 0;
            transition: opacity 0.2s;
        }
        .template-card:hover::before { opacity: 1; }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .card-title {
            font-size: 1rem;
            font-weight: 600;
            color: #f0f6fc;
            margin: 0;
        }
        .card-description {
            font-size: 0.875rem;
            color: #8b949e;
            line-height: 1.5;
            margin: 8px 0 16px;
        }
        .card-footer {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: auto;
        }

        /* ── Badges ────────────────────────────────────────────────── */
        .badge {
            display: inline-block;
            border-radius: 6px;
            padding: 3px 10px;
            font-size: 0.75rem;
            font-weight: 500;
            line-height: 1.5;
        }
        .badge-category {
            background: rgba(88,166,255,0.15);
            color: #58a6ff;
            border: 1px solid rgba(88,166,255,0.25);
        }
        .badge-tag {
            background: rgba(139,148,158,0.12);
            color: #8b949e;
            border: 1px solid rgba(139,148,158,0.2);
        }
        .badge-easy   { background: rgba(34,197,94,0.15);  color: #22c55e; border: 1px solid rgba(34,197,94,0.25); }
        .badge-medium { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.25); }
        .badge-hard   { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.25); }

        /* ── Section headings ──────────────────────────────────────── */
        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #f0f6fc;
            margin: 24px 0 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-divider {
            border: none;
            border-top: 1px solid #30363d;
            margin: 24px 0;
        }

        /* ── Stat cards ────────────────────────────────────────────── */
        .stat-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #58a6ff;
        }
        .stat-label {
            font-size: 0.85rem;
            color: #8b949e;
            margin-top: 4px;
        }

        /* ── YAML viewer ───────────────────────────────────────────── */
        .yaml-container {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 10px;
            overflow: hidden;
        }
        .yaml-toolbar {
            background: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .yaml-filename {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #8b949e;
        }

        /* ── Info boxes ────────────────────────────────────────────── */
        .info-box {
            background: rgba(88,166,255,0.08);
            border: 1px solid rgba(88,166,255,0.25);
            border-radius: 10px;
            padding: 16px 20px;
            margin: 12px 0;
        }
        .info-box-title {
            font-weight: 600;
            color: #58a6ff;
            margin-bottom: 6px;
            font-size: 0.9rem;
        }
        .info-box-body {
            color: #c9d1d9;
            font-size: 0.875rem;
            line-height: 1.6;
        }
        .warning-box {
            background: rgba(245,158,11,0.08);
            border: 1px solid rgba(245,158,11,0.25);
            border-radius: 10px;
            padding: 16px 20px;
            margin: 12px 0;
        }
        .warning-box-title {
            font-weight: 600;
            color: #f59e0b;
            margin-bottom: 6px;
            font-size: 0.9rem;
        }
        .warning-box-body {
            color: #c9d1d9;
            font-size: 0.875rem;
            line-height: 1.6;
        }

        /* ── Learn concept cards ───────────────────────────────────── */
        .concept-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
        }
        .concept-icon {
            font-size: 2rem;
            margin-bottom: 12px;
        }
        .concept-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #f0f6fc;
            margin-bottom: 8px;
        }
        .concept-body {
            font-size: 0.875rem;
            color: #8b949e;
            line-height: 1.6;
        }

        /* ── Streamlit widget overrides ────────────────────────────── */
        .stButton > button {
            background: linear-gradient(135deg, #238636, #2ea043);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: opacity 0.2s;
            width: 100%;
        }
        .stButton > button:hover {
            opacity: 0.85;
            color: white;
        }
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #1f6feb, #388bfd);
            color: white !important;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: opacity 0.2s;
            width: 100%;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            opacity: 0.85;
        }
        .stTextInput input, .stSelectbox select {
            background: #161b22 !important;
            border-color: #30363d !important;
            color: #f0f6fc !important;
        }
        .stRadio > div {
            gap: 4px;
        }
        .stRadio > div > label {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 8px 16px;
            color: #c9d1d9 !important;
            transition: border-color 0.2s;
        }
        .stRadio > div > label:hover {
            border-color: #58a6ff;
        }
        [data-testid="stExpander"] {
            background: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
