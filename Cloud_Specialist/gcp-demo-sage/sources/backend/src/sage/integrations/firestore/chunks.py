"""Reads and writes on the `chunks` collection in Firestore."""

from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.firestore.client import get_firestore_client


def find_nearest_chunks(embedding: list[float]) -> list[Chunk]:
    """Retrieves the nearest document chunks using Firestore Vector Search."""
    config = get_app_config()
    db = get_firestore_client()
    collection_ref = db.collection(config.firestore_collection)

    vector_query = collection_ref.find_nearest(
        vector_field="embedding",
        query_vector=Vector(embedding),
        distance_measure=DistanceMeasure.COSINE,
        limit=config.top_k,
    )

    docs = vector_query.stream()
    chunks = []
    for doc in docs:
        data = doc.to_dict()
        chunks.append(
            Chunk(
                id=doc.id,
                text=data.get("text", ""),
                source=data.get("source", ""),
                section=data.get("section"),
                chunk_index=data.get("chunk_index", 0),
            )
        )
    return chunks


def delete_chunks_for_source(source: str) -> None:
    """Remove existing chunks for a document to allow safe re-ingestion."""
    config = get_app_config()
    db = get_firestore_client()
    collection_ref = db.collection(config.firestore_collection)
    
    docs = collection_ref.where("source", "==", source).stream()
    for doc in docs:
        doc.reference.delete()


def add_chunk(
    chunk_id: str,
    text: str,
    embedding: list[float],
    source: str,
    section: str | None,
    chunk_index: int,
) -> None:
    """Persist a document chunk with its vector embedding to Firestore."""
    config = get_app_config()
    db = get_firestore_client()
    doc_ref = db.collection(config.firestore_collection).document(chunk_id)
    
    doc_ref.set({
        "text": text,
        "embedding": Vector(embedding),
        "source": source,
        "section": section,
        "chunk_index": chunk_index,
    })