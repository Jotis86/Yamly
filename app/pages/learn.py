"""Learn page — educational content about GitHub Actions concepts."""

import streamlit as st


def render_learn() -> None:
    st.markdown(
        """
        <div style="margin-bottom:24px;">
            <h1 style="color:#f0f6fc; font-size:1.8rem; margin:0;">📚 Aprende GitHub Actions</h1>
            <p style="color:#8b949e; margin:6px 0 0; font-size:0.9rem;">
                Conceptos clave, buenas prácticas y ejemplos para dominar GitHub Actions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔑 Conceptos clave", "⚡ Eventos & Triggers", "🔐 Secretos & Variables", "✅ Buenas prácticas"]
    )

    # ── Tab 1: Core concepts ──────────────────────────────────────────────────
    with tab1:
        _concepts_section()

    # ── Tab 2: Events & Triggers ──────────────────────────────────────────────
    with tab2:
        _events_section()

    # ── Tab 3: Secrets & Variables ────────────────────────────────────────────
    with tab3:
        _secrets_section()

    # ── Tab 4: Best practices ─────────────────────────────────────────────────
    with tab4:
        _best_practices_section()


# ── Section renderers ─────────────────────────────────────────────────────────

def _concepts_section() -> None:
    st.markdown("<br/>", unsafe_allow_html=True)

    concepts = [
        ("🗂️", "Workflow", "Un archivo YAML en <code>.github/workflows/</code> que define la automatización completa. Puede tener múltiples jobs."),
        ("💼", "Job", "Conjunto de steps que se ejecutan en el mismo runner. Los jobs corren en paralelo por defecto, o en secuencia con <code>needs:</code>."),
        ("🏃", "Runner", "El servidor virtual donde se ejecuta un job. GitHub ofrece <code>ubuntu-latest</code>, <code>windows-latest</code> y <code>macos-latest</code>."),
        ("🔧", "Step", "La unidad mínima de trabajo. Puede ejecutar un comando shell (<code>run:</code>) o una Action reutilizable (<code>uses:</code>)."),
        ("📦", "Action", "Un componente reutilizable publicado en el Marketplace de GitHub. Ejemplo: <code>actions/checkout@v4</code>."),
        ("🌍", "Context", "Variables disponibles en el workflow como <code>github.ref</code>, <code>github.sha</code>, <code>runner.os</code>, etc."),
        ("📊", "Matrix", "Estrategia para ejecutar el mismo job con diferentes combinaciones de parámetros (ej: múltiples versiones de Python)."),
        ("🏷️", "Environment", "Entorno lógico (staging, production) con sus propias variables, secretos y reglas de protección."),
    ]

    cols = st.columns(2)
    for i, (icon, title, body) in enumerate(concepts):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="concept-card">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                        <span style="font-size:1.4rem;">{icon}</span>
                        <span class="concept-title" style="margin:0;">{title}</span>
                    </div>
                    <div class="concept-body">{body}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Matrix example
    st.markdown(
        "<div class='section-title' style='margin-top:24px;'>📊 Ejemplo: Matrix Strategy</div>",
        unsafe_allow_html=True,
    )
    st.code(
        """\
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # Esto genera 6 combinaciones (3 versiones × 2 OS)
""",
        language="yaml",
    )


def _events_section() -> None:
    st.markdown("<br/>", unsafe_allow_html=True)

    events = [
        ("push", "Se activa al hacer push a una o más ramas o tags.", """\
on:
  push:
    branches: [main, develop]
    tags: ["v*.*.*"]
    paths:
      - "src/**"
      - "!docs/**"  # excluye docs"""),
        ("pull_request", "Se activa ante eventos en Pull Requests.", """\
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]"""),
        ("schedule", "Ejecuta el workflow en una programación cron.", """\
on:
  schedule:
    - cron: "0 8 * * 1-5"  # 8am cada día de semana
    - cron: "0 0 * * 0"    # medianoche cada domingo"""),
        ("workflow_dispatch", "Permite ejecutar el workflow manualmente desde la UI.", """\
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Entorno de despliegue"
        required: true
        default: "staging"
        type: choice
        options: [staging, production]"""),
        ("release", "Se activa cuando se crea, edita o publica un Release.", """\
on:
  release:
    types: [published, created, edited]"""),
        ("workflow_call", "Permite que otro workflow llame a este (workflows reutilizables).", """\
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_token:
        required: true"""),
    ]

    for event_name, description, code_example in events:
        with st.expander(f"⚡ `{event_name}`  —  {description}"):
            st.code(code_example, language="yaml")

    st.markdown(
        """
        <div class="info-box" style="margin-top:16px;">
            <div class="info-box-title">💡 Consejo: paths-filter</div>
            <div class="info-box-body">
                Usa <code>paths:</code> y <code>paths-ignore:</code> para evitar ejecutar workflows
                cuando solo cambian archivos irrelevantes (ej: documentación, imágenes).
                Esto ahorra minutos de GitHub Actions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _secrets_section() -> None:
    st.markdown("<br/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">🔐 Secretos (Secrets)</div>
                <div class="concept-body">
                    Valores cifrados almacenados en GitHub. Se acceden con
                    <code>${{ secrets.NOMBRE }}</code>. Nunca aparecen en logs.
                    <br/><br/>
                    <strong>Tipos:</strong><br/>
                    • <strong>Repository secrets:</strong> Solo ese repo<br/>
                    • <strong>Environment secrets:</strong> Ligados a un entorno<br/>
                    • <strong>Organization secrets:</strong> Compartidos entre repos
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">📋 Variables (Variables)</div>
                <div class="concept-body">
                    Valores no cifrados para configuración reutilizable. Se acceden con
                    <code>${{ vars.NOMBRE }}</code>. Visibles en logs.
                    <br/><br/>
                    <strong>Contextos automáticos (<code>${{ github.* }}</code>):</strong><br/>
                    • <code>github.repository</code><br/>
                    • <code>github.ref_name</code><br/>
                    • <code>github.sha</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='section-title' style='margin-top:8px;'>💻 Ejemplos de uso</div>",
        unsafe_allow_html=True,
    )

    ex1, ex2 = st.columns(2)
    with ex1:
        st.markdown("**Usar secretos en un step:**")
        st.code(
            """\
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_URL: ${{ secrets.DATABASE_URL }}
        run: ./deploy.sh
""",
            language="yaml",
        )

    with ex2:
        st.markdown("**GITHUB_TOKEN — token automático:**")
        st.code(
            """\
jobs:
  create-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # necesario para crear releases
    steps:
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          # GITHUB_TOKEN es generado automáticamente
          token: ${{ secrets.GITHUB_TOKEN }}
""",
            language="yaml",
        )

    st.markdown(
        """
        <div class="warning-box">
            <div class="warning-box-title">⚠️ Principio de menor privilegio</div>
            <div class="warning-box-body">
                Siempre declara los <code>permissions:</code> mínimos necesarios para cada job.
                Por defecto, <code>GITHUB_TOKEN</code> tiene permisos de solo lectura.
                Agrega solo los permisos que realmente necesitas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _best_practices_section() -> None:
    st.markdown("<br/>", unsafe_allow_html=True)

    practices = [
        (
            "🔒",
            "Fija las versiones de Actions",
            "Usa un SHA de commit completo en lugar de etiquetas mutables para evitar ataques de supply chain.",
            """\
# ❌ Inseguro — la etiqueta puede cambiar
- uses: actions/checkout@main

# ✅ Seguro — SHA inmutable
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
""",
        ),
        (
            "⚡",
            "Usa caché para acelerar workflows",
            "Cachea dependencias para reducir tiempos de ejecución hasta un 80%.",
            """\
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip          # ← caché automático de pip

- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm          # ← caché automático de npm
""",
        ),
        (
            "🎯",
            "Filtra por paths para ahorrar minutos",
            "Evita ejecutar el workflow completo cuando solo cambian archivos irrelevantes.",
            """\
on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "tests/**"
      - "requirements.txt"
    paths-ignore:
      - "docs/**"
      - "*.md"
      - ".gitignore"
""",
        ),
        (
            "🔄",
            "Usa concurrency para evitar deployments duplicados",
            "Cancela workflows en progreso cuando llega uno nuevo al mismo entorno.",
            """\
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true   # cancela el anterior

# Para production, mejor esperar en lugar de cancelar:
concurrency:
  group: production
  cancel-in-progress: false
""",
        ),
        (
            "🛡️",
            "Valida entradas en workflow_dispatch",
            "Nunca uses inputs del usuario directamente en comandos shell sin validación.",
            """\
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]  # ← valores controlados
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}  # ← uso seguro
""",
        ),
        (
            "🏗️",
            "Reutiliza workflows con workflow_call",
            "Extrae lógica común en workflows reutilizables para DRY y mantenibilidad.",
            """\
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string

# En otro workflow:
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets: inherit
""",
        ),
    ]

    for icon, title, description, code in practices:
        with st.expander(f"{icon} {title}"):
            st.markdown(
                f'<p style="color:#8b949e; font-size:0.875rem; margin-bottom:12px;">{description}</p>',
                unsafe_allow_html=True,
            )
            st.code(code, language="yaml")

    # Useful links
    st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-title'>🔗 Recursos útiles</div>",
        unsafe_allow_html=True,
    )

    links = [
        ("📖", "Documentación oficial de GitHub Actions", "https://docs.github.com/actions"),
        ("🛒", "GitHub Actions Marketplace", "https://github.com/marketplace?type=actions"),
        ("🔐", "Hardening de seguridad", "https://docs.github.com/actions/security-guides/security-hardening-for-github-actions"),
        ("📊", "Uso de GitHub Actions (facturación)", "https://docs.github.com/billing/managing-billing-for-github-actions"),
        ("🔁", "Workflows reutilizables", "https://docs.github.com/actions/sharing-automations/reusing-workflows"),
        ("🏆", "Actions de inicio rápido", "https://github.com/actions/starter-workflows"),
    ]

    link_cols = st.columns(3)
    for i, (icon, label, url) in enumerate(links):
        with link_cols[i % 3]:
            st.markdown(
                f"""
                <a href="{url}" target="_blank"
                   style="display:block; background:#161b22; border:1px solid #30363d;
                          border-radius:10px; padding:14px 16px; text-decoration:none;
                          color:#c9d1d9; font-size:0.85rem; margin-bottom:12px;
                          transition:border-color 0.2s;"
                   onmouseover="this.style.borderColor='#58a6ff'"
                   onmouseout="this.style.borderColor='#30363d'">
                    <span style="font-size:1.2rem;">{icon}</span>&nbsp; {label}
                    <span style="color:#58a6ff; float:right;">→</span>
                </a>
                """,
                unsafe_allow_html=True,
            )
