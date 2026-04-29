"""YAML viewer and download component for a single template."""

import streamlit as st
from app.templates.models import Template
from app.config import DIFFICULTY_LABELS


def render_template_viewer(template: Template) -> None:
    """Render the full detail view for a template with YAML code and download."""
    diff_icon = DIFFICULTY_LABELS.get(template.difficulty, {}).get("icon", "")

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:#161b22; border:1px solid #30363d; border-radius:12px;
             padding:24px; margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <h2 style="color:#f0f6fc; margin:0; font-size:1.5rem;">{template.name}</h2>
                <span class="badge badge-category">{template.category}</span>
                <span class="badge badge-{'easy' if template.difficulty=='Principiante' else 'medium' if template.difficulty=='Intermedio' else 'hard'}">
                    {diff_icon} {template.difficulty}
                </span>
            </div>
            <p style="color:#8b949e; margin:12px 0 0; font-size:0.9rem;">{template.description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Two-column layout: info + download ────────────────────────────────────
    col_info, col_dl = st.columns([2, 1])

    with col_info:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-box-title">🎯 ¿Qué hace?</div>
                <div class="info-box-body">{template.what_it_does}</div>
            </div>
            <div class="warning-box">
                <div class="warning-box-title">💡 ¿Cuándo usarlo?</div>
                <div class="warning-box-body">{template.when_to_use}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_dl:
        st.markdown(
            f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:20px;">
                <div style="font-size:0.8rem; font-weight:600; color:#8b949e;
                     text-transform:uppercase; letter-spacing:0.06em; margin-bottom:16px;">
                    📥 Descargar plantilla
                </div>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.75rem; color:#8b949e; margin-bottom:4px;">Guardar en:</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#58a6ff;
                         background:#0d1117; border:1px solid #30363d; border-radius:6px; padding:8px 12px;">
                        .github/workflows/<br/>{template.filename}
                    </div>
                </div>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.75rem; color:#8b949e; margin-bottom:4px;">Eventos:</div>
            """,
            unsafe_allow_html=True,
        )
        for event in template.trigger_events:
            st.markdown(
                f'<span class="badge badge-tag" style="display:block; margin-bottom:4px;">⚡ {event}</span>',
                unsafe_allow_html=True,
            )
        st.markdown("</div></div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Descargar .yml",
            data=template.yaml_content,
            file_name=template.filename,
            mime="text/yaml",
            key=f"dl_{template.id}",
        )

        # Tags
        st.markdown(
            "<div style='margin-top:16px;'>",
            unsafe_allow_html=True,
        )
        tags_html = " ".join(
            f'<span class="badge badge-tag">#{t}</span>' for t in template.tags
        )
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── YAML Viewer ───────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="margin-top:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;
                 background:#161b22; border:1px solid #30363d; border-radius:10px 10px 0 0;
                 padding:10px 16px;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#8b949e;">
                    📄 .github/workflows/{template.filename}
                </span>
                <span class="badge badge-tag">YAML</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(template.yaml_content, language="yaml")
