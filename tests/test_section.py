"""Tests for RFC Section dataclass."""

from rfc_editor import RFCSection


class TestRFCSection:
    """Tests for RFCSection class."""

    def test_default_creation(self):
        """Test creating an RFCSection with defaults."""
        section = RFCSection()
        assert section.number == ""
        assert section.title == ""
        assert section.content == ""

    def test_creation_with_values(self):
        """Test creating an RFCSection with values."""
        section = RFCSection(
            number="1",
            title="Introduction",
            content="This is the introduction content.",
        )
        assert section.number == "1"
        assert section.title == "Introduction"
        assert section.content == "This is the introduction content."

    def test_to_dict(self):
        """Test converting RFCSection to dictionary."""
        section = RFCSection(
            number="2.1",
            title="Requirements Language",
            content="RFC 2119 keywords...",
        )
        result = section.to_dict()
        assert result == {
            "number": "2.1",
            "title": "Requirements Language",
            "content": "RFC 2119 keywords...",
        }

    def test_nested_sections(self):
        """Test nested section numbers."""
        section = RFCSection(
            number="1.2.3", title="Deep Section", content="..."
        )
        assert section.number == "1.2.3"
        assert section.title == "Deep Section"

    def test_content_with_newlines(self):
        """Test content with multiple paragraphs."""
        content = "First paragraph.\n\nSecond paragraph."
        section = RFCSection(number="1", title="Test", content=content)
        assert "\n" in section.content
