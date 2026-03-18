"""Tests for the web_intel module.

Validates URL validation, output schema, body text sanitization, and
graceful handling of missing scrapling dependency.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

# Make web_intel importable
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "skills" / "web-intelligence" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

import web_intel  # noqa: E402


class TestURLValidation:
    """Verify URL validation accepts http/https and rejects others."""

    def test_http_accepted(self) -> None:
        assert web_intel.validate_url("http://example.com") is True

    def test_https_accepted(self) -> None:
        assert web_intel.validate_url("https://example.com/page?q=1") is True

    def test_file_rejected(self) -> None:
        assert web_intel.validate_url("file:///etc/passwd") is False

    def test_ftp_rejected(self) -> None:
        assert web_intel.validate_url("ftp://files.example.com/data") is False

    def test_empty_rejected(self) -> None:
        assert web_intel.validate_url("") is False

    def test_no_scheme_rejected(self) -> None:
        assert web_intel.validate_url("example.com") is False


class TestOutputSchema:
    """Test that analyse_url returns the required keys."""

    def test_required_keys_present(self) -> None:
        mock_result = {
            "url": "https://example.com",
            "title": "Example",
            "body_text": "Hello world",
            "links": [],
            "sentiment": 0.0,
            "word_count": 2,
        }
        with mock.patch.object(web_intel, "_fetch_and_parse", return_value=mock_result):
            result = web_intel.analyse_url("https://example.com")
            for key in ("url", "title", "body_text", "links", "word_count"):
                assert key in result, f"Missing key: {key}"


class TestBodySanitization:
    """Test that script and style tags are stripped from body text."""

    def test_strips_script_tags(self) -> None:
        html = "<html><body><p>Hello</p><script>alert('xss')</script><p>World</p></body></html>"
        result = web_intel.sanitize_body(html)
        assert "alert" not in result
        assert "Hello" in result
        assert "World" in result

    def test_strips_style_tags(self) -> None:
        html = "<html><body><style>.red{color:red}</style><p>Content</p></body></html>"
        result = web_intel.sanitize_body(html)
        assert "color:red" not in result
        assert "Content" in result

    def test_empty_html(self) -> None:
        result = web_intel.sanitize_body("")
        assert result == ""


class TestMissingScrapling:
    """Ensure the module handles missing scrapling gracefully."""

    def test_scrapling_available_flag_exists(self) -> None:
        assert hasattr(web_intel, "SCRAPLING_AVAILABLE")
        assert isinstance(web_intel.SCRAPLING_AVAILABLE, bool)

    def test_analyse_without_scrapling(self) -> None:
        """analyse_url should return a result even without scrapling."""
        with mock.patch.object(web_intel, "SCRAPLING_AVAILABLE", False):
            result = web_intel.analyse_url("https://example.com")
            assert isinstance(result, dict)
            assert "url" in result
