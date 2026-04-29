"""GitHub Actions Hub — Streamlit entry point."""

import streamlit as st
from app.config import APP_TITLE, APP_ICON
from app.components.styles import inject_global_styles
from app.components.sidebar import render_sidebar
from app.pages.home import render_home
from app.pages.explorer import render_explorer
from app.pages.learn import render_learn


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_global_styles()

    # Initialize session state
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = None

    # Render sidebar and get current page
    page = render_sidebar()

    # Route to page
    if page == "home":
        render_home()
    elif page == "explorer":
        render_explorer()
    elif page == "learn":
        render_learn()


if __name__ == "__main__":
    main()

