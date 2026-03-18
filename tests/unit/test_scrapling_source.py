"""Tests for the scrapling_source module.

Validates import guards, sentiment scoring, URL validation, and the
fetch_live_topics function schema using mocked HTTP responses.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

# Make scrapling_source importable
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "skills" / "mindspider-connector" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

import scrapling_source  # noqa: E402


class TestImportGuard:
    """Verify the SCRAPLING_AVAILABLE flag behaves correctly."""

    def test_scrapling_available_is_bool(self) -> None:
        """SCRAPLING_AVAILABLE should be a boolean regardless of install state."""
        assert isinstance(scrapling_source.SCRAPLING_AVAILABLE, bool)

    def test_module_loads_without_scrapling(self) -> None:
        """Module must load even when scrapling is not installed."""
        with mock.patch.dict(sys.modules, {"scrapling": None}):
            import importlib

            reloaded = importlib.reload(scrapling_source)
            assert hasattr(reloaded, "SCRAPLING_AVAILABLE")


class TestSentimentScoring:
    """Test sentiment_score with known inputs."""

    def test_positive_text(self) -> None:
        score = scrapling_source.sentiment_score("This is absolutely wonderful and amazing")
        assert isinstance(score, float)
        assert score > 0

    def test_negative_text(self) -> None:
        score = scrapling_source.sentiment_score("This is terrible awful and horrible")
        assert isinstance(score, float)
        assert score < 0

    def test_neutral_text(self) -> None:
        score = scrapling_source.sentiment_score("The meeting is at 3pm today")
        assert isinstance(score, float)
        assert score == 0.0

    def test_empty_text(self) -> None:
        score = scrapling_source.sentiment_score("")
        assert score == 0.0


class TestURLValidation:
    """Test validate_url rejects bad URLs and accepts good ones."""

    def test_valid_http(self) -> None:
        assert scrapling_source.validate_url("http://example.com") is True

    def test_valid_https(self) -> None:
        assert scrapling_source.validate_url("https://example.com/path") is True

    def test_rejects_file_protocol(self) -> None:
        assert scrapling_source.validate_url("file:///etc/passwd") is False

    def test_rejects_empty(self) -> None:
        assert scrapling_source.validate_url("") is False


class TestFetchLiveTopics:
    """Test fetch_live_topics returns the expected schema."""

    @mock.patch.object(scrapling_source, "SCRAPLING_AVAILABLE", False)
    def test_returns_empty_without_scrapling(self) -> None:
        """Without scrapling, fetch_live_topics should return an empty list."""
        result = scrapling_source.fetch_live_topics(domain="AI")
        assert isinstance(result, list)
        assert len(result) == 0

    @mock.patch.object(scrapling_source, "SCRAPLING_AVAILABLE", True)
    def test_schema_keys(self) -> None:
        """Each topic dict should have the expected keys when scrapers return data."""
        mock_topic = {
            "topic": "Test Topic",
            "sentiment_score": 0.5,
            "post_count": 100,
            "trend_direction": "rising",
            "sample_posts": ["post1"],
            "platforms": ["reddit"],
            "first_seen": "2026-03-15T00:00:00Z",
            "peak_time": "2026-03-15T01:00:00Z",
        }
        mock_fetcher = mock.MagicMock()
        with mock.patch("scrapling_source.Fetcher", return_value=mock_fetcher, create=True):
            with mock.patch.object(scrapling_source, "_scrape_reddit", return_value=[mock_topic]):
                with mock.patch.object(scrapling_source, "_scrape_hackernews", return_value=[]):
                    with mock.patch.object(scrapling_source, "_scrape_bluesky", return_value=[]):
                        result = scrapling_source.fetch_live_topics(domain=None)
                        assert len(result) >= 1
                        for topic in result:
                            assert "topic" in topic
                            assert "sentiment_score" in topic
                            assert "post_count" in topic
