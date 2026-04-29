"""Template card component for the explorer grid."""

import streamlit as st
from app.templates.models import Template
from app.config import DIFFICULTY_LABELS


def _difficulty_badge_class(difficulty: str) -> str:
    mapping = {"Principiante": "easy", "Intermedio": "medium", "Avanzado": "hard"}
    return mapping.get(difficulty, "easy")


def render_template_card(template: Template) -> bool:
    """
    Render a single template card. Returns True if the user clicked 'Ver plantilla'.
    """
    diff_class = _difficulty_badge_class(template.difficulty)
    diff_icon = DIFFICULTY_LABELS.get(template.difficulty, {}).get("icon", "")
    tags_html = " ".join(
        f'<span class="badge badge-tag">#{t}</span>' for t in template.tags[:4]
    )

    st.markdown(
        f"""
        <div class="template-card">
            <div class="card-header">
                <div>
                    <p class="card-title">{template.name}</p>
                    <span class="badge badge-category">{template.category}</span>
                    &nbsp;
                    <span class="badge badge-{diff_class}">{diff_icon} {template.difficulty}</span>
                </div>
            </div>
            <p class="card-description">{template.description}</p>
            <div class="card-footer">{tags_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Small spacer between card HTML and the button
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    return st.button("Ver plantilla →", key=f"btn_{template.id}")
