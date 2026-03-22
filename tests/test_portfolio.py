import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from app.portfolio import Portfolio


@pytest.fixture
def mock_csv(tmp_path):
    """Create a temporary CSV for testing."""
    csv_path = tmp_path / "test_portfolio.csv"
    pd.DataFrame({
        "Techstack": ["Python/Machine Learning", "React/Frontend", "DevOps/Docker"],
        "Links": [
            "https://github.com/user/ml-project",
            "https://github.com/user/react-app",
            "https://github.com/user/devops-project",
        ],
    }).to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def portfolio(mock_csv, tmp_path):
    """Portfolio instance using temp storage."""
    with patch("app.portfolio.chromadb.PersistentClient") as mock_client:
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        p = Portfolio(file_path=mock_csv)
        p.collection = mock_collection
        return p


def test_portfolio_loads_csv(portfolio):
    assert len(portfolio.data) == 3
    assert "Techstack" in portfolio.data.columns
    assert "Links" in portfolio.data.columns


def test_load_portfolio_adds_records(portfolio):
    portfolio.collection.count.return_value = 0
    portfolio.load_portfolio()
    assert portfolio.collection.add.call_count == 3


def test_load_portfolio_skips_if_already_loaded(portfolio):
    portfolio.collection.count.return_value = 3
    portfolio.load_portfolio()
    portfolio.collection.add.assert_not_called()


def test_query_links_calls_collection(portfolio):
    portfolio.collection.count.return_value = 3
    portfolio.collection.query.return_value = {
        "metadatas": [[{"links": "https://github.com/user/ml-project"}]]
    }
    result = portfolio.query_links(["Python machine learning"])
    portfolio.collection.query.assert_called_once()
    assert len(result) == 1


def test_query_links_empty_skills_returns_empty(portfolio):
    result = portfolio.query_links([])
    assert result == []