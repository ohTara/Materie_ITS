"""Text embedding via Vertex AI (Google Gen AI SDK)."""

from functools import lru_cache
from google import genai
from sage.config import get_app_config


@lru_cache
def _get_genai_client() -> genai.Client:
    config = get_app_config()
    # Aggiunto vertexai=True per abilitare l'integrazione Vertex AI su GCP
    return genai.Client(vertexai=True, project=config.project_id, location=config.region)


def embed_text(text: str) -> list[float]:
    """Generate a vector embedding using Vertex AI text-embedding model."""
    config = get_app_config()
    client = _get_genai_client()
    response = client.models.embed_content(
        model=config.embedding_model,
        contents=text,
    )
    return response.embeddings[0].values