"""Template explorer page with filtering, search and YAML preview."""

import streamlit as st
from app.config import CATEGORIES, CATEGORY_ICONS
from app.templates.catalog import (
    get_all_templates,
    get_templates_by_category,
    search_templates,
    get_template_by_id,
)
from app.components.cards import render_template_card
from app.components.viewer import render_template_viewer


def render_explorer() -> None:
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-bottom:24px;">
            <h1 style="color:#f0f6fc; font-size:1.8rem; margin:0;">📦 Explorador de Plantillas</h1>
            <p style="color:#8b949e; margin:6px 0 0; font-size:0.9rem;">
                12 plantillas de GitHub Actions listas para copiar y usar en tus proyectos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── If a template is selected, show its detail view ───────────────────────
    if "selected_template" in st.session_state and st.session_state.selected_template:
        _render_detail_view()
        return

    # ── Filter & search bar ───────────────────────────────────────────────────
    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        category = st.selectbox(
            "Filtrar por categoría",
            options=CATEGORIES,
            format_func=lambda c: f"{CATEGORY_ICONS.get(c, '📁')} {c}",
        )
    with search_col:
        query = st.text_input(
            "Buscar plantilla",
            placeholder="ej: docker, deploy, python...",
        )

    # Combine filters
    if query.strip():
        templates = search_templates(query)
        if category != "Todos":
            templates = [t for t in templates if t.category == category]
    else:
        templates = get_templates_by_category(category)

    # ── Results count ─────────────────────────────────────────────────────────
    result_label = f"{len(templates)} plantilla{'s' if len(templates) != 1 else ''} encontrada{'s' if len(templates) != 1 else ''}"
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:8px; margin:16px 0 8px;">
            <span style="color:#8b949e; font-size:0.85rem;">{result_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not templates:
        st.markdown(
            """
            <div style="text-align:center; padding:60px 20px; color:#8b949e;">
                <div style="font-size:3rem;">🔍</div>
                <div style="font-size:1rem; margin-top:12px;">No se encontraron plantillas.</div>
                <div style="font-size:0.85rem; margin-top:6px;">Intenta con otro término o categoría.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Template grid (3 columns) ─────────────────────────────────────────────
    cols_per_row = 3
    for row_start in range(0, len(templates), cols_per_row):
        row_templates = templates[row_start : row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, template in zip(cols, row_templates):
            with col:
                clicked = render_template_card(template)
                if clicked:
                    st.session_state.selected_template = template.id
                    st.rerun()

    # ── Download all button ───────────────────────────────────────────────────
    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:8px;">
            <p style="color:#8b949e; font-size:0.85rem;">
                ¿Quieres todas las plantillas de una vez?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    all_templates = get_all_templates()
    all_yaml = "\n\n# " + "─" * 60 + "\n\n".join(
        f"# {t.name}\n# Guardar en: .github/workflows/{t.filename}\n\n{t.yaml_content}"
        for t in all_templates
    )
    dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])
    with dl_col2:
        st.download_button(
            label="📥 Descargar todas las plantillas (.txt)",
            data=all_yaml,
            file_name="github-actions-templates.txt",
            mime="text/plain",
            key="dl_all",
        )


def _render_detail_view() -> None:
    """Render the single-template detail view with a back button."""
    # Back button
    if st.button("← Volver al explorador"):
        st.session_state.selected_template = None
        st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    template = get_template_by_id(st.session_state.selected_template)
    if template is None:
        st.error("Plantilla no encontrada.")
        st.session_state.selected_template = None
        return

    render_template_viewer(template)

    # ── Related templates ──────────────────────────────────────────────────────
    all_templates = get_all_templates()
    related = [t for t in all_templates if t.category == template.category and t.id != template.id]
    if related:
        st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-title'>📂 Plantillas relacionadas</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(min(len(related), 3))
        for col, rel in zip(cols, related[:3]):
            with col:
                clicked = render_template_card(rel)
                if clicked:
                    st.session_state.selected_template = rel.id
                    st.rerun()
