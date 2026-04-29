"""Home / landing page."""

import streamlit as st
from app.config import APP_TITLE, APP_SUBTITLE, CATEGORY_ICONS, CATEGORIES
from app.templates.catalog import get_all_templates


def render_home() -> None:
    templates = get_all_templates()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-title">⚡ {APP_TITLE}</div>
            <p class="hero-subtitle">{APP_SUBTITLE}</p>
            <span class="hero-badge">🆓 100% Gratuito</span>
            <span class="hero-badge">📦 {len(templates)} Plantillas listas</span>
            <span class="hero-badge">🔒 Mejores prácticas incluidas</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Stats row ─────────────────────────────────────────────────────────────
    categories = {t.category for t in templates}
    difficulties = {t.difficulty for t in templates}
    c1, c2, c3, c4 = st.columns(4)
    _stat(c1, str(len(templates)), "Plantillas")
    _stat(c2, str(len(categories)), "Categorías")
    _stat(c3, str(len(difficulties)), "Niveles")
    _stat(c4, "100%", "Listas para usar")

    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

    # ── What is GitHub Actions? ───────────────────────────────────────────────
    st.markdown(
        "<div class='section-title'>🤔 ¿Qué es GitHub Actions?</div>",
        unsafe_allow_html=True,
    )
    col_text, col_code = st.columns([1, 1])
    with col_text:
        st.markdown(
            """
            <div style="color:#c9d1d9; font-size:0.9rem; line-height:1.8;">
                <p>
                    <strong style="color:#f0f6fc;">GitHub Actions</strong> es la plataforma de
                    automatización de GitHub que te permite crear flujos de trabajo (workflows)
                    que se ejecutan automáticamente ante eventos en tu repositorio.
                </p>
                <p>Con GitHub Actions puedes:</p>
                <ul style="margin-top:8px;">
                    <li>✅ Ejecutar tests automáticamente en cada PR</li>
                    <li>🚀 Desplegar tu app al hacer push a main</li>
                    <li>🔒 Analizar vulnerabilidades de seguridad</li>
                    <li>🤖 Automatizar tareas repetitivas</li>
                    <li>📦 Publicar paquetes y releases</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_code:
        st.code(
            """\
# Estructura básica de un workflow
name: Mi Primer Workflow

on:
  push:
    branches: [main]

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "¡Hola, GitHub Actions!"
""",
            language="yaml",
        )

    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

    # ── Workflow anatomy ──────────────────────────────────────────────────────
    st.markdown(
        "<div class='section-title'>🔬 Anatomía de un Workflow</div>",
        unsafe_allow_html=True,
    )
    a1, a2, a3, a4 = st.columns(4)
    _anatomy_card(a1, "⚡", "Evento (on:)", "El disparador del workflow. Puede ser un push, PR, cron o evento manual.")
    _anatomy_card(a2, "💼", "Job", "Un conjunto de steps que se ejecutan en el mismo runner de forma secuencial.")
    _anatomy_card(a3, "🏃", "Runner", "El servidor donde se ejecuta el job. Ej: ubuntu-latest, windows-latest.")
    _anatomy_card(a4, "🔧", "Step", "Una acción individual: un comando shell o una Action reutilizable.")

    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

    # ── Categories preview ────────────────────────────────────────────────────
    st.markdown(
        "<div class='section-title'>📂 Categorías de plantillas</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(CATEGORIES) - 1)
    for i, cat in enumerate(CATEGORIES[1:]):
        icon = CATEGORY_ICONS.get(cat, "📁")
        count = sum(1 for t in templates if t.category == cat)
        with cols[i]:
            st.markdown(
                f"""
                <div class="stat-card" style="cursor:default;">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#f0f6fc; margin-top:8px;">{cat}</div>
                    <div style="font-size:0.8rem; color:#8b949e;">{count} plantillas</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

    # ── Quick start guide ─────────────────────────────────────────────────────
    st.markdown(
        "<div class='section-title'>🚀 Guía de inicio rápido</div>",
        unsafe_allow_html=True,
    )
    s1, s2, s3, s4 = st.columns(4)
    _step_card(s1, "1", "Elige una plantilla", "Ve a la sección Plantillas y selecciona la que más se adapte a tu proyecto.")
    _step_card(s2, "2", "Revisa el YAML", "Examina el workflow, entiende cada bloque y ajusta los parámetros necesarios.")
    _step_card(s3, "3", "Descarga el archivo", "Usa el botón de descarga para obtener el archivo .yml listo para usar.")
    _step_card(s4, "4", "Súbelo a tu repo", "Coloca el archivo en .github/workflows/ y haz commit. ¡Listo!")


# ── Helper components ──────────────────────────────────────────────────────────

def _stat(col, value: str, label: str) -> None:
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _anatomy_card(col, icon: str, title: str, body: str) -> None:
    with col:
        st.markdown(
            f"""
            <div class="concept-card">
                <div class="concept-icon">{icon}</div>
                <div class="concept-title">{title}</div>
                <div class="concept-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _step_card(col, number: str, title: str, body: str) -> None:
    with col:
        st.markdown(
            f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:20px;">
                <div style="width:32px; height:32px; background:linear-gradient(135deg,#1f6feb,#388bfd);
                     border-radius:50%; display:flex; align-items:center; justify-content:center;
                     color:white; font-weight:700; font-size:0.9rem; margin-bottom:12px;">{number}</div>
                <div style="font-size:0.9rem; font-weight:600; color:#f0f6fc; margin-bottom:6px;">{title}</div>
                <div style="font-size:0.8rem; color:#8b949e; line-height:1.5;">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
