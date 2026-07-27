from unittest.mock import AsyncMock, MagicMock

import pytest
from simpson_retrieval.service import (
    PostgresHybridRetrievalService,
    RetrievalQuery,
)


@pytest.mark.asyncio
async def test_search_exact_match():
    service = PostgresHybridRetrievalService(db_session=AsyncMock())
    query = RetrievalQuery(text_query="LUS28", limit=10)

    results = await service.search(query)

    assert len(results) == 1
    assert results[0].retrieval_method == "EXACT"
    assert results[0].subject_id == "prod-LUS28"
    assert results[0].score == 1.0
    service.db_session.execute.assert_not_called()


@pytest.mark.asyncio
async def test_search_hybrid_rrf():
    mock_db = AsyncMock()

    mock_row_1 = MagicMock()
    mock_row_1.subject_id = "prod-H1A"
    mock_row_1.title = "Simpson Strong-Tie H1A Hurricane Tie"
    mock_row_1.content_excerpt = "High-wind rafter to top-plate connection tie."
    mock_row_1.rrf_score = 0.033

    mock_row_2 = MagicMock()
    mock_row_2.subject_id = "prod-LUS28"
    mock_row_2.title = "Simpson Strong-Tie LUS28 Joist Hanger"
    mock_row_2.content_excerpt = "Double 2x8 joist hanger with speed prongs."
    mock_row_2.rrf_score = 0.016

    mock_db.execute.return_value = [mock_row_1, mock_row_2]

    service = PostgresHybridRetrievalService(db_session=mock_db)
    query = RetrievalQuery(
        text_query="hurricane ties for rafters long query", limit=10, embedding=[0.1, 0.2, 0.3]
    )

    results = await service.search(query)

    assert len(results) == 2
    assert results[0].retrieval_method == "HYBRID_RRF"
    assert results[0].subject_id == "prod-H1A"
    assert results[0].score == 0.033

    assert results[1].retrieval_method == "HYBRID_RRF"
    assert results[1].subject_id == "prod-LUS28"
    assert results[1].score == 0.016

    mock_db.execute.assert_called_once()
    args, kwargs = mock_db.execute.call_args
    sql_text = args[0].text
    params = args[1]

    assert "WITH lexical_search AS" in sql_text
    assert "vector_search AS" in sql_text
    assert "FULL OUTER JOIN vector_search v ON l.subject_id = v.subject_id" in sql_text

    assert params["text_query"] == "HURRICANE TIES FOR RAFTERS LONG QUERY"
    assert params["query_embedding"] == "[0.1, 0.2, 0.3]"
    assert params["limit"] == 10
    assert params["k"] == 60


@pytest.mark.asyncio
async def test_search_no_db_session():
    service = PostgresHybridRetrievalService(db_session=None)
    query = RetrievalQuery(text_query="hurricane ties for rafters long query", limit=10)

    results = await service.search(query)

    assert results == []
