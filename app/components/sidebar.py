"""Sidebar navigation component."""

import streamlit as st
from app.config import APP_TITLE, APP_ICON, VERSION, PAGES, CATEGORIES, CATEGORY_ICONS
from app.templates.catalog import get_all_templates


def render_sidebar() -> str:
    """Render the sidebar and return the selected page key."""
    with st.sidebar:
        # Brand
        st.markdown(
            f"""
            <div style="text-align:center; padding: 16px 0 8px;">
                <div style="font-size:2.5rem;">{APP_ICON}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#f0f6fc;">{APP_TITLE}</div>
                <div style="font-size:0.75rem; color:#8b949e;">v{VERSION}</div>
            </div>
            <hr style="border-color:#30363d; margin: 12px 0;" />
            """,
            unsafe_allow_html=True,
        )

        # Navigation
        st.markdown(
            "<div style='font-size:0.75rem; font-weight:600; color:#8b949e; "
            "text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>Navegación</div>",
            unsafe_allow_html=True,
        )
        selected = st.radio(
            label="nav",
            options=list(PAGES.keys()),
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:#30363d; margin: 16px 0;' />", unsafe_allow_html=True)

        # Quick stats
        templates = get_all_templates()
        categories = {t.category for t in templates}
        st.markdown(
            f"""
            <div style="background:#0d1117; border:1px solid #30363d; border-radius:10px; padding:16px;">
                <div style="font-size:0.75rem; font-weight:600; color:#8b949e; text-transform:uppercase;
                     letter-spacing:0.08em; margin-bottom:12px;">Estadísticas</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="color:#8b949e; font-size:0.85rem;">Plantillas</span>
                    <span style="color:#58a6ff; font-weight:600;">{len(templates)}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#8b949e; font-size:0.85rem;">Categorías</span>
                    <span style="color:#58a6ff; font-weight:600;">{len(categories)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border-color:#30363d; margin: 16px 0;' />", unsafe_allow_html=True)

        # Categories legend
        st.markdown(
            "<div style='font-size:0.75rem; font-weight:600; color:#8b949e; "
            "text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>Categorías</div>",
            unsafe_allow_html=True,
        )
        for cat in CATEGORIES[1:]:  # skip "Todos"
            icon = CATEGORY_ICONS.get(cat, "📁")
            count = sum(1 for t in templates if t.category == cat)
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                     padding:4px 0; color:#c9d1d9; font-size:0.85rem;">
                    <span>{icon} {cat}</span>
                    <span style="background:#30363d; color:#8b949e; border-radius:10px;
                          padding:1px 8px; font-size:0.75rem;">{count}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="margin-top:24px; text-align:center;">
                <a href="https://docs.github.com/actions" target="_blank"
                   style="color:#58a6ff; font-size:0.8rem; text-decoration:none;">
                    📖 Documentación oficial →
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return PAGES[selected]
