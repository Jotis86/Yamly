<div align="center">

![Yamly Banner](image/banner.png)

# ⚡ Yamly

**Aprende, explora y descarga plantillas de GitHub Actions listas para usar**

[![Lint](https://github.com/Jotis86/yamly/actions/workflows/lint.yml/badge.svg)](https://github.com/Jotis86/yamly/actions/workflows/lint.yml)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-FF4B4B?logo=streamlit&logoColor=white)
![Ruff](https://img.shields.io/badge/linter-ruff-D7FF64?logo=ruff&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## ¿Qué es Yamly?

Yamly es una aplicación web construida con **Streamlit** que actúa como hub de referencia para **GitHub Actions**. Ofrece tres secciones principales:

- 🏠 **Inicio** — visión general de las categorías y acceso rápido a las plantillas
- 📦 **Plantillas** — 12 workflows listos para copiar, filtrar por categoría y descargar
- 📚 **Aprende** — guía educativa con conceptos clave, eventos, secretos y buenas prácticas

---

## Plantillas incluidas

| # | Nombre | Categoría | Nivel |
|---|--------|-----------|-------|
| 1 | Python CI | CI/CD | 🟢 Principiante |
| 2 | Node.js CI | CI/CD | 🟢 Principiante |
| 3 | Docker Build & Push | CI/CD | 🟡 Intermedio |
| 4 | Deploy to GitHub Pages | Despliegue | 🟢 Principiante |
| 5 | Auto Release | Automatización | 🟡 Intermedio |
| 6 | CodeQL Security Scan | Seguridad | 🟡 Intermedio |
| 7 | Dependabot Auto-merge | Automatización | 🟡 Intermedio |
| 8 | PR Auto-labeler | Automatización | 🟢 Principiante |
| 9 | Stale Issues & PRs | Automatización | 🟢 Principiante |
| 10 | Multi-environment Deploy | Despliegue | 🔴 Avanzado |
| 11 | Super Linter | Calidad de Código | 🟢 Principiante |
| 12 | SonarCloud Analysis | Calidad de Código | 🟡 Intermedio |

---

## Puesta en marcha

### Con uv (recomendado)

```bash
# Instalar dependencias
uv sync

# Ejecutar la app
uv run streamlit run main.py
```

### Con Docker

```bash
# Construir y levantar
docker compose up --build

# Solo levantar (si la imagen ya existe)
docker compose up
```

La app queda disponible en **http://localhost:8501**.

---

## Estructura del proyecto

```
yamly/
├── main.py                   # Entrypoint de Streamlit
├── pyproject.toml            # Dependencias y configuración
├── Dockerfile                # Build multi-stage con uv
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── lint.yml          # Ruff en cada push/PR
└── app/
    ├── config.py             # Constantes globales
    ├── components/           # Estilos, sidebar, cards, viewer
    ├── pages/                # home, explorer, learn
    └── templates/            # Modelos y catálogo de plantillas
```

---

## CI

Cada push y pull request ejecuta **Ruff** automáticamente mediante la action oficial [`astral-sh/ruff-action`](https://github.com/astral-sh/ruff-action). La configuración se lee directamente desde `pyproject.toml`.

---

## Stack

- **[Streamlit](https://streamlit.io/)** — framework de la interfaz web
- **[uv](https://github.com/astral-sh/uv)** — gestión de dependencias y entornos
- **[Ruff](https://github.com/astral-sh/ruff)** — linter y formatter de Python
- **[Docker](https://www.docker.com/)** — contenedorización con build multi-stage
