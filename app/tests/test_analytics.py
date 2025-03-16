import pytest
from unittest.mock import MagicMock
from app.analytics import analyze_notes
from app.models import Note


@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    mock_notes = [
        Note(id=1, content="First example note with several words in it."),
        Note(id=2, content="Which is slightly longer than the first one."),
        Note(id=3, content="Short example."),
    ]
    mock_session.query.return_value.all.return_value = mock_notes
    return mock_session


def test_analyze_notes(mock_db_session):
    result = analyze_notes(mock_db_session)

    assert result["total_notes"] == 3
    assert result["total_word_count"] == 18
    assert result["avg_note_length"] == 6.0
    assert len(result["most_common_words"]) > 0
    assert len(result["longest_notes"]) == 3
    assert len(result["shortest_notes"]) == 3
