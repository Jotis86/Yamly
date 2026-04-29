"""Application-wide configuration constants."""

APP_TITLE = "GitHub Actions Hub"
APP_SUBTITLE = "Aprende, explora y descarga plantillas de GitHub Actions listas para usar"
APP_ICON = "⚡"
VERSION = "1.0.0"

CATEGORIES = [
    "Todos",
    "CI/CD",
    "Seguridad",
    "Automatización",
    "Despliegue",
    "Calidad de Código",
]

DIFFICULTY_LABELS = {
    "Principiante": {"color": "#22c55e", "icon": "🟢"},
    "Intermedio": {"color": "#f59e0b", "icon": "🟡"},
    "Avanzado": {"color": "#ef4444", "icon": "🔴"},
}

CATEGORY_ICONS = {
    "CI/CD": "🔄",
    "Seguridad": "🔒",
    "Automatización": "🤖",
    "Despliegue": "🚀",
    "Calidad de Código": "✅",
    "Todos": "⚡",
}

PAGES = {
    "🏠 Inicio": "home",
    "📦 Plantillas": "explorer",
    "📚 Aprende": "learn",
}
