"""Catalog of 12 ready-to-use GitHub Actions templates."""

from app.templates.models import Template

# ── 1. Python CI ──────────────────────────────────────────────────────────────
_PYTHON_CI_YAML = """\
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test & Lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff

      - name: Lint with Ruff
        run: ruff check .

      - name: Run tests with coverage
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
"""

# ── 2. Node.js CI ─────────────────────────────────────────────────────────────
_NODEJS_CI_YAML = """\
name: Node.js CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    name: Build & Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Build application
        run: npm run build
"""

# ── 3. Docker Build & Push ────────────────────────────────────────────────────
_DOCKER_YAML = """\
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ["v*.*.*"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
"""

# ── 4. Deploy to GitHub Pages ─────────────────────────────────────────────────
_PAGES_YAML = """\
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    name: Build Site
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    name: Deploy to Pages
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""

# ── 5. Auto Release ───────────────────────────────────────────────────────────
_RELEASE_YAML = """\
name: Auto Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --verbose --latest
        env:
          OUTPUT: CHANGELOG.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
          draft: false
          prerelease: ${{ contains(github.ref, '-alpha') || contains(github.ref, '-beta') }}
          generate_release_notes: true
"""

# ── 6. CodeQL Security Scan ───────────────────────────────────────────────────
_CODEQL_YAML = """\
name: CodeQL Security Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 8 * * 1"

jobs:
  analyze:
    name: Analyze Code
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [python, javascript]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-and-quality

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
"""

# ── 7. Dependabot Auto-merge ──────────────────────────────────────────────────
_DEPENDABOT_YAML = """\
name: Dependabot Auto-merge

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    name: Auto-merge Dependabot PRs
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'

    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Approve minor and patch updates
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr review --approve "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Auto-merge minor and patch updates
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

# ── 8. PR Labeler ─────────────────────────────────────────────────────────────
_PR_LABELER_YAML = """\
name: PR Auto-labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    name: Label Pull Request
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Label PR based on changed files
        uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
          sync-labels: true

      - name: Add size label
        uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_max_size: 10
          s_max_size: 100
          m_max_size: 500
          l_max_size: 1000
          fail_if_xl: false
"""

# ── 9. Stale Issues & PRs Cleanup ─────────────────────────────────────────────
_STALE_YAML = """\
name: Stale Issues & PRs Cleanup

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    name: Mark and Close Stale Items
    runs-on: ubuntu-latest

    steps:
      - name: Mark stale issues and PRs
        uses: actions/stale@v9
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-issue-message: >
            Este issue no ha tenido actividad en 30 días y será cerrado
            en 7 días si no recibe más actividad. ¡Gracias por tu contribución!
          stale-pr-message: >
            Este PR no ha tenido actividad en 30 días y será cerrado
            en 7 días si no recibe más actividad.
          close-issue-message: "Issue cerrado por inactividad."
          close-pr-message: "PR cerrado por inactividad."
          days-before-stale: 30
          days-before-close: 7
          stale-issue-label: stale
          stale-pr-label: stale
          exempt-issue-labels: "pinned,security,roadmap"
          exempt-pr-labels: "pinned,wip"
"""

# ── 10. Multi-environment Deploy ──────────────────────────────────────────────
_MULTI_DEPLOY_YAML = """\
name: Multi-environment Deploy

on:
  push:
    branches:
      - develop
      - main

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment..."
          # Replace with your actual deployment script

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to production
        run: |
          echo "Deploying to production environment..."
          # Replace with your actual deployment script
"""

# ── 11. Super Linter ──────────────────────────────────────────────────────────
_SUPER_LINTER_YAML = """\
name: Super Linter

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  super-lint:
    name: Lint Code Base
    runs-on: ubuntu-latest
    permissions:
      contents: read
      statuses: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Super Linter
        uses: super-linter/super-linter@v7
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          VALIDATE_ALL_CODEBASE: false
          VALIDATE_PYTHON_RUFF: true
          VALIDATE_JAVASCRIPT_ES: true
          VALIDATE_TYPESCRIPT_ES: true
          VALIDATE_YAML: true
          VALIDATE_JSON: true
          VALIDATE_MARKDOWN: true
          VALIDATE_DOCKERFILE_HADOLINT: true
"""

# ── 12. SonarCloud Analysis ───────────────────────────────────────────────────
_SONARCLOUD_YAML = """\
name: SonarCloud Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    name: SonarCloud Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies and run tests
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
          pytest --cov=. --cov-report=xml

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
"""

# ── Template catalog ──────────────────────────────────────────────────────────

TEMPLATES: list[Template] = [
    Template(
        id="python-ci",
        name="Python CI",
        description="Pipeline de integración continua para proyectos Python con tests, cobertura y linting.",
        category="CI/CD",
        difficulty="Principiante",
        tags=["python", "pytest", "ruff", "codecov", "matrix"],
        yaml_content=_PYTHON_CI_YAML,
        what_it_does=(
            "Ejecuta linting con Ruff y tests con pytest (incluyendo reporte de cobertura) "
            "en múltiples versiones de Python usando una estrategia de matrix."
        ),
        when_to_use=(
            "Ideal para cualquier proyecto Python que use pytest como framework de tests. "
            "Úsalo desde el inicio del proyecto para mantener calidad de código."
        ),
        filename="python-ci.yml",
        trigger_events=["push", "pull_request"],
    ),
    Template(
        id="nodejs-ci",
        name="Node.js CI",
        description="Pipeline de CI para proyectos Node.js con instalación, lint, tests y build.",
        category="CI/CD",
        difficulty="Principiante",
        tags=["nodejs", "npm", "testing", "matrix", "build"],
        yaml_content=_NODEJS_CI_YAML,
        what_it_does=(
            "Instala dependencias con npm ci, ejecuta el linter, corre los tests "
            "y compila la aplicación en múltiples versiones de Node.js."
        ),
        when_to_use=(
            "Para proyectos Node.js, React, Vue, Angular u otros frameworks JS/TS. "
            "Asegura que el código funciona en las versiones LTS de Node."
        ),
        filename="nodejs-ci.yml",
        trigger_events=["push", "pull_request"],
    ),
    Template(
        id="docker-build-push",
        name="Docker Build & Push",
        description="Construye una imagen Docker y la publica en GitHub Container Registry (GHCR).",
        category="CI/CD",
        difficulty="Intermedio",
        tags=["docker", "ghcr", "containers", "registry", "metadata"],
        yaml_content=_DOCKER_YAML,
        what_it_does=(
            "Construye la imagen Docker con caché de GitHub Actions, extrae metadatos "
            "automáticos (tags semver) y la publica en GHCR con permisos mínimos."
        ),
        when_to_use=(
            "Para proyectos que se distribuyen como contenedores Docker. "
            "Úsalo cuando quieras publicar imágenes con cada push a main o con cada tag de versión."
        ),
        filename="docker-build-push.yml",
        trigger_events=["push (main, tags v*.*.*)"],
    ),
    Template(
        id="github-pages",
        name="Deploy to GitHub Pages",
        description="Compila y despliega automáticamente un sitio estático en GitHub Pages.",
        category="Despliegue",
        difficulty="Principiante",
        tags=["pages", "static-site", "deploy", "nodejs", "artifacts"],
        yaml_content=_PAGES_YAML,
        what_it_does=(
            "Construye el sitio con npm run build, sube el artefacto de Pages "
            "y lo despliega usando el entorno oficial de GitHub Pages con OIDC."
        ),
        when_to_use=(
            "Para documentación, portafolios o cualquier sitio estático (Vite, Next.js, Astro, etc.) "
            "alojado en GitHub Pages. Sin necesidad de tokens externos."
        ),
        filename="deploy-pages.yml",
        trigger_events=["push (main)", "workflow_dispatch"],
    ),
    Template(
        id="auto-release",
        name="Auto Release",
        description="Crea releases de GitHub automáticamente al hacer push de un tag semver.",
        category="Automatización",
        difficulty="Intermedio",
        tags=["release", "changelog", "semver", "git-cliff", "tags"],
        yaml_content=_RELEASE_YAML,
        what_it_does=(
            "Al pushear un tag v*.*.*, genera el changelog con git-cliff "
            "y crea el Release de GitHub con las notas de cambios y soporte para pre-releases."
        ),
        when_to_use=(
            "Para proyectos con versionado semántico que quieren automatizar el proceso "
            "de releases. Muy útil en librerías y herramientas CLI."
        ),
        filename="auto-release.yml",
        trigger_events=["push (tags v*.*.*)"],
    ),
    Template(
        id="codeql-security",
        name="CodeQL Security Scan",
        description="Análisis de seguridad del código con CodeQL para detectar vulnerabilidades.",
        category="Seguridad",
        difficulty="Intermedio",
        tags=["codeql", "security", "sast", "vulnerabilities", "schedule"],
        yaml_content=_CODEQL_YAML,
        what_it_does=(
            "Ejecuta el análisis CodeQL (SAST) de GitHub en múltiples lenguajes, "
            "detectando vulnerabilidades de seguridad y malas prácticas de código. "
            "Se ejecuta en PRs, pushes y cada lunes automáticamente."
        ),
        when_to_use=(
            "Para cualquier proyecto que quiera detectar vulnerabilidades de seguridad (OWASP). "
            "Esencial en proyectos públicos o con requerimientos de compliance."
        ),
        filename="codeql-analysis.yml",
        trigger_events=["push", "pull_request", "schedule (lunes)"],
    ),
    Template(
        id="dependabot-automerge",
        name="Dependabot Auto-merge",
        description="Aprueba y fusiona automáticamente actualizaciones de parches y menores de Dependabot.",
        category="Automatización",
        difficulty="Intermedio",
        tags=["dependabot", "auto-merge", "dependencies", "semver", "security"],
        yaml_content=_DEPENDABOT_YAML,
        what_it_does=(
            "Detecta PRs de Dependabot, verifica el tipo de actualización (semver minor/patch) "
            "y los aprueba y fusiona automáticamente, evitando el trabajo manual de mergear actualizaciones pequeñas."
        ),
        when_to_use=(
            "Para proyectos que usan Dependabot y quieren reducir la carga manual "
            "de revisar actualizaciones de seguridad y parches menores."
        ),
        filename="dependabot-automerge.yml",
        trigger_events=["pull_request"],
    ),
    Template(
        id="pr-labeler",
        name="PR Auto-labeler",
        description="Etiqueta automáticamente los Pull Requests según los archivos modificados y su tamaño.",
        category="Automatización",
        difficulty="Principiante",
        tags=["labels", "pull-request", "automation", "dx", "triage"],
        yaml_content=_PR_LABELER_YAML,
        what_it_does=(
            "Aplica labels en PRs según los archivos modificados (configurado en .github/labeler.yml) "
            "y también agrega etiquetas de tamaño (XS, S, M, L, XL) según el número de líneas cambiadas."
        ),
        when_to_use=(
            "Para equipos que quieren tener sus PRs organizados automáticamente. "
            "Muy útil en repositorios monorepo o proyectos con múltiples áreas."
        ),
        filename="pr-labeler.yml",
        trigger_events=["pull_request (opened, synchronize, reopened)"],
    ),
    Template(
        id="stale-cleanup",
        name="Stale Issues & PRs",
        description="Marca y cierra automáticamente issues y PRs inactivos después de 30 días.",
        category="Automatización",
        difficulty="Principiante",
        tags=["stale", "cleanup", "issues", "pull-request", "schedule"],
        yaml_content=_STALE_YAML,
        what_it_does=(
            "Cada día a medianoche, marca como 'stale' los issues y PRs sin actividad "
            "en 30 días y los cierra automáticamente 7 días después si siguen sin actividad."
        ),
        when_to_use=(
            "Para proyectos open source o con muchos colaboradores donde el backlog "
            "de issues puede crecer descontroladamente. Mantiene el repositorio limpio."
        ),
        filename="stale-cleanup.yml",
        trigger_events=["schedule (diario)", "workflow_dispatch"],
    ),
    Template(
        id="multi-env-deploy",
        name="Multi-environment Deploy",
        description="Pipeline de despliegue a staging (develop) y producción (main) con entornos de GitHub.",
        category="Despliegue",
        difficulty="Avanzado",
        tags=["deploy", "staging", "production", "environments", "aws", "multi-env"],
        yaml_content=_MULTI_DEPLOY_YAML,
        what_it_does=(
            "Despliega automáticamente a staging cuando se hace push a develop "
            "y a producción cuando se hace push a main, usando entornos de GitHub "
            "con URLs de deployment y credenciales de AWS Secrets."
        ),
        when_to_use=(
            "Para proyectos con flujo GitFlow o trunk-based que necesitan despliegues "
            "diferenciados por entorno. Base ideal para cualquier pipeline de CD en AWS."
        ),
        filename="multi-env-deploy.yml",
        trigger_events=["push (develop → staging, main → production)"],
    ),
    Template(
        id="super-linter",
        name="Super Linter",
        description="Ejecuta múltiples linters en paralelo sobre Python, JS/TS, YAML, JSON, Markdown y Dockerfile.",
        category="Calidad de Código",
        difficulty="Principiante",
        tags=["linting", "ruff", "eslint", "yaml", "markdown", "dockerfile", "super-linter"],
        yaml_content=_SUPER_LINTER_YAML,
        what_it_does=(
            "Ejecuta Super Linter de GitHub, que orquesta múltiples linters (Ruff para Python, "
            "ESLint para JS/TS, yamllint, markdownlint, Hadolint para Dockerfiles) "
            "solo sobre los archivos modificados en cada PR o push."
        ),
        when_to_use=(
            "Para proyectos multi-lenguaje que quieren imponer estándares de estilo y calidad "
            "sin configurar cada linter por separado. Ideal al incorporar nuevos colaboradores."
        ),
        filename="super-linter.yml",
        trigger_events=["push", "pull_request"],
    ),
    Template(
        id="sonarcloud",
        name="SonarCloud Analysis",
        description="Análisis estático de código con SonarCloud: cobertura, deuda técnica y quality gates.",
        category="Calidad de Código",
        difficulty="Intermedio",
        tags=["sonarcloud", "sast", "coverage", "quality-gate", "technical-debt"],
        yaml_content=_SONARCLOUD_YAML,
        what_it_does=(
            "Ejecuta los tests con cobertura y envía los resultados a SonarCloud, "
            "que analiza bugs, code smells, duplicaciones y deuda técnica. "
            "Bloquea el PR si no pasa el quality gate configurado."
        ),
        when_to_use=(
            "Para equipos que quieren métricas de calidad continuas y quality gates en PRs. "
            "Requiere crear un proyecto en sonarcloud.io y añadir SONAR_TOKEN como secreto "
            "y un archivo sonar-project.properties en la raíz del repositorio."
        ),
        filename="sonarcloud.yml",
        trigger_events=["push", "pull_request"],
    ),
]


def get_all_templates() -> list[Template]:
    """Return the full template catalog."""
    return TEMPLATES


def get_templates_by_category(category: str) -> list[Template]:
    """Return templates filtered by category. 'Todos' returns all."""
    if category == "Todos":
        return TEMPLATES
    return [t for t in TEMPLATES if t.category == category]


def get_template_by_id(template_id: str) -> Template | None:
    """Return a single template by its id, or None if not found."""
    return next((t for t in TEMPLATES if t.id == template_id), None)


def search_templates(query: str) -> list[Template]:
    """Return templates matching the search query (name, tags, description)."""
    q = query.lower().strip()
    if not q:
        return TEMPLATES
    return [
        t
        for t in TEMPLATES
        if q in t.name.lower()
        or q in t.description.lower()
        or any(q in tag for tag in t.tags)
        or q in t.category.lower()
    ]
