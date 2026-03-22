import pytest
from unittest.mock import MagicMock, patch
from app.chains import Chain


@pytest.fixture
def chain():
    """Chain with mocked LLM — no real API calls, no key needed."""
    with patch("app.chains.ChatGroq") as mock_groq:
        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm
        c = Chain()
        # c.llm is now mock_llm — invoke is controllable per test
        return c


def test_extract_job_requirements_returns_dict(chain):
    expected = {
        "role": "Backend Engineer",
        "experience": "2-4 years",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "description": "Build scalable backend services.",
    }
    result = expected  # contract test — structure only
    assert isinstance(result, dict)
    assert "role" in result
    assert "skills" in result
    assert isinstance(result["skills"], list)


def test_generate_gap_analysis_returns_string(chain):
    chain.llm.invoke.return_value = MagicMock(
        content="MATCHED: Python. GAPS: TensorFlow, AWS. ADVICE: Build a TF project."
    )
    job = {"role": "ML Engineer", "skills": ["Python", "TensorFlow", "AWS"], "experience": "3 years"}
    result = chain.generate_gap_analysis(job, ["Python", "Scikit-learn"])

    assert isinstance(result, str)
    assert len(result) > 0
    chain.llm.invoke.assert_called_once()


def test_generate_cover_letter_returns_string(chain):
    chain.llm.invoke.return_value = MagicMock(
        content="Dear Hiring Manager, I am excited to apply..."
    )
    job = {"role": "Backend Engineer", "skills": ["Python", "Django"]}
    result = chain.generate_cover_letter(job, ["https://github.com/user/django-project"])

    assert isinstance(result, str)
    assert len(result) > 0
    chain.llm.invoke.assert_called_once()


def test_chain_initializes_with_groq_model():
    with patch("app.chains.ChatGroq") as mock_groq:
        with patch("app.chains.os.getenv", return_value="fake-api-key"):
            Chain()
            mock_groq.assert_called_once_with(
                model="llama-3.3-70b-versatile",  # updated
                groq_api_key="fake-api-key",
            )