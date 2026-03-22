import pytest
from app.utils import clean_text

def test_removes_html_tags():
    assert clean_text("<h1>Software Engineer</h1>") == "Software Engineer"

def test_removes_urls():
    assert clean_text("Visit https://example.com for details") == "Visit for details".strip()

def test_removes_special_characters():
    result = clean_text("Skills: Python, AWS & Docker!")
    assert "&" not in result
    assert "!" not in result

def test_collapses_whitespace():
    result = clean_text("hello    world")
    assert result == "hello world"

def test_empty_string():
    assert clean_text("") == ""

def test_plain_text_unchanged():
    text = "Python machine learning experience required"
    assert clean_text(text) == text