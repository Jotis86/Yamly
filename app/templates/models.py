"""Data models for GitHub Actions templates."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Template:
    """Represents a GitHub Actions workflow template."""

    id: str
    name: str
    description: str
    category: str
    difficulty: str
    tags: List[str]
    yaml_content: str
    what_it_does: str
    when_to_use: str
    filename: str
    trigger_events: List[str] = field(default_factory=list)

    def get_download_name(self) -> str:
        """Return the recommended .github/workflows filename."""
        return self.filename
