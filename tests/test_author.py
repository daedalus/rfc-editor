"""Tests for RFC Author dataclass."""

from rfc_editor import RFCAuthor


class TestRFCAuthor:
    """Tests for RFCAuthor class."""

    def test_default_creation(self):
        """Test creating an RFCAuthor with defaults."""
        author = RFCAuthor()
        assert author.name == ""
        assert author.organization == ""
        assert author.email == ""
        assert author.address == ""

    def test_creation_with_values(self):
        """Test creating an RFCAuthor with values."""
        author = RFCAuthor(
            name="John Doe",
            organization="Example Corp",
            email="john@example.com",
            address="123 Main St",
        )
        assert author.name == "John Doe"
        assert author.organization == "Example Corp"
        assert author.email == "john@example.com"
        assert author.address == "123 Main St"

    def test_to_dict(self):
        """Test converting RFCAuthor to dictionary."""
        author = RFCAuthor(
            name="Jane Doe",
            organization="Test Org",
            email="jane@test.com",
        )
        result = author.to_dict()
        assert result == {
            "name": "Jane Doe",
            "organization": "Test Org",
            "email": "jane@test.com",
            "address": "",
        }

    def test_to_dict_with_empty(self):
        """Test converting empty RFCAuthor to dictionary."""
        author = RFCAuthor()
        result = author.to_dict()
        assert result == {
            "name": "",
            "organization": "",
            "email": "",
            "address": "",
        }
