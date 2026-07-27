"""Retrieval engine interfaces: exact matching, pg_trgm lexical search, pgvector semantic search."""

from simpson_retrieval.service import RetrievalQuery, RetrievalResult, RetrievalService

__all__ = ["RetrievalQuery", "RetrievalResult", "RetrievalService"]
