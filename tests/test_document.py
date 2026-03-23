"""Tests for RFC Document dataclass."""

from rfc_editor import RFCDocument, RFCSection


class TestRFCDocument:
    """Tests for RFCDocument class."""

    def test_default_creation(self):
        """Test creating an RFCDocument with defaults."""
        doc = RFCDocument()
        assert doc.rfc_number == ""
        assert doc.category == ""
        assert doc.title == ""
        assert doc.abstract == ""
        assert doc.authors == []
        assert doc.status_of_memo == ""
        assert doc.copyright_notice == ""
        assert doc.toc == ""
        assert doc.sections == []
        assert doc.acknowledgements == ""
        assert doc.contributors == ""
        assert doc.index == ""
        assert doc.authors_address == ""
        assert doc.raw_content == ""

    def test_creation_with_values(self):
        """Test creating an RFCDocument with values."""
        doc = RFCDocument(
            rfc_number="1234",
            category="Standards Track",
            title="Test RFC",
            abstract="This is an abstract.",
        )
        assert doc.rfc_number == "1234"
        assert doc.category == "Standards Track"
        assert doc.title == "Test RFC"
        assert doc.abstract == "This is an abstract."

    def test_get_section_existing(self):
        """Test getting an existing section."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
            RFCSection(
                number="2", title="Requirements", content="Req content"
            ),
        ]
        section = doc.get_section("1")
        assert section is not None
        assert section.number == "1"
        assert section.title == "Introduction"

    def test_get_section_nonexistent(self):
        """Test getting a non-existent section."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
        ]
        section = doc.get_section("999")
        assert section is None

    def test_get_section_by_title_exact(self):
        """Test getting a section by exact title."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
            RFCSection(
                number="2",
                title="Requirements Language",
                content="Req content",
            ),
        ]
        section = doc.get_section_by_title("Introduction")
        assert section is not None
        assert section.number == "1"

    def test_get_section_by_title_partial(self):
        """Test getting a section by partial title match."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
            RFCSection(
                number="2",
                title="Requirements Language",
                content="Req content",
            ),
        ]
        section = doc.get_section_by_title("Requirements")
        assert section is not None
        assert section.number == "2"

    def test_get_section_by_title_case_insensitive(self):
        """Test getting a section by title is case-insensitive."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
        ]
        section = doc.get_section_by_title("INTRODUCTION")
        assert section is not None
        assert section.number == "1"

    def test_get_section_by_title_nonexistent(self):
        """Test getting a non-existent section by title."""
        doc = RFCDocument()
        doc.sections = [
            RFCSection(
                number="1",
                title="Introduction",
                content="Intro content",
            ),
        ]
        section = doc.get_section_by_title("NonExistent")
        assert section is None
