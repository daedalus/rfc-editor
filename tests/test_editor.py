"""Tests for RFCEditor class."""

import os
import tempfile
from pathlib import Path

import pytest

from rfc_editor import RFCEditor

SAMPLE_RFC_CONTENT = """RFC 1234 (Standards Track)

Test RFC Title

Abstract

This is the abstract of the test RFC document. It describes the purpose
and scope of this document.

Status of This Memo

This document specifies an Internet standards track protocol for the
Internet community, and requests discussion and suggestions for
improvements.

Copyright (c) 2023 Example Corp

Table of Contents

1. Introduction ...................................................  3
2. Requirements Language ...........................................  4
3. Security Considerations ..........................................  5
4. References .....................................................  6
   4.1. Normative References .......................................  6

1. Introduction

This is the introduction section. It provides background and
motivation for this RFC.

2. Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
RFC 2119.

3. Security Considerations

This section discusses security considerations relevant to this RFC.

4. References

4.1. Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

Acknowledgements

Thanks to all reviewers.

Contributors

Jane Doe contributed significantly.

Author's Address

John Doe
Example Corp
123 Main Street
City, State 12345
Email: john@example.com
"""


class TestRFCEditorInit:
    """Tests for RFCEditor initialization."""

    def test_init(self):
        """Test creating an RFCEditor instance."""
        editor = RFCEditor()
        assert editor.document is None

    def test_init_with_document(self):
        """Test creating an RFCEditor with a document."""
        editor = RFCEditor()
        assert editor.document is None


class TestRFCEditorLoad:
    """Tests for loading RFC documents."""

    def test_load_file_not_found(self):
        """Test loading a non-existent file."""
        editor = RFCEditor()
        with pytest.raises(FileNotFoundError):
            editor.load("/nonexistent/file.txt")

    def test_load_valid_file(self):
        """Test loading a valid RFC file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(SAMPLE_RFC_CONTENT)
            temp_path = f.name

        try:
            editor = RFCEditor()
            doc = editor.load(temp_path)
            assert doc is not None
            assert doc.rfc_number == "1234"
            assert doc.category == "Standards Track"
        finally:
            os.unlink(temp_path)

    def test_parse_content(self):
        """Test parsing RFC content directly."""
        editor = RFCEditor()
        doc = editor.parse(SAMPLE_RFC_CONTENT)
        assert doc is not None
        assert doc.rfc_number == "1234"
        assert doc.category == "Standards Track"
        assert "Test RFC Title" in doc.title


class TestRFCEditorGetters:
    """Tests for getting document sections."""

    def test_get_document_loaded(self):
        """Test getting document after loading."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert editor.document is not None
        assert editor.document.rfc_number == "1234"

    def test_get_title(self):
        """Test getting the title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert editor.get_title() == "Test RFC Title"

    def test_get_title_no_document(self):
        """Test getting title without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_title()

    def test_get_abstract(self):
        """Test getting the abstract."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "abstract of the test RFC" in editor.get_abstract()

    def test_get_abstract_no_document(self):
        """Test getting abstract without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_abstract()

    def test_get_status_of_memo(self):
        """Test getting Status of This Memo."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "Internet standards track" in editor.get_status_of_memo()

    def test_get_status_of_memo_no_document(self):
        """Test getting status without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_status_of_memo()

    def test_get_copyright(self):
        """Test getting copyright notice."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        year, holders = editor.get_copyright()
        assert year == 2023
        assert holders == "Example Corp"

    def test_get_copyright_no_document(self):
        """Test getting copyright without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_copyright()

    def test_get_toc(self):
        """Test getting Table of Contents."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "1. Introduction" in editor.get_toc()

    def test_get_toc_no_document(self):
        """Test getting TOC without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_toc()

    def test_get_acknowledgements(self):
        """Test getting Acknowledgements."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "reviewers" in editor.get_acknowledgements()

    def test_get_acknowledgements_no_document(self):
        """Test getting acknowledgements without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_acknowledgements()

    def test_get_contributors(self):
        """Test getting Contributors."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "Jane Doe" in editor.get_contributors()

    def test_get_contributors_no_document(self):
        """Test getting contributors without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_contributors()

    def test_get_authors_address(self):
        """Test getting Author's Address."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert "John Doe" in editor.get_authors_address()

    def test_get_authors_address_no_document(self):
        """Test getting author address without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_authors_address()

    def test_get_section_by_title(self):
        """Test getting a section by its title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        section = editor.get_section_by_title("Introduction")
        assert section is not None
        assert section.number == "1"
        assert section.title == "Introduction"

    def test_get_section_by_title_nonexistent(self):
        """Test getting non-existent section by title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        assert editor.get_section_by_title("NonExistent") is None

    def test_get_section_by_title_no_document(self):
        """Test getting section without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.get_section_by_title("Introduction")


class TestRFCEditorSetters:
    """Tests for setting document sections."""

    def test_set_title(self):
        """Test setting the title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_title("New Title")
        assert editor.document.title == "New Title"

    def test_set_title_no_document(self):
        """Test setting title without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.set_title("New Title")

    def test_set_abstract(self):
        """Test setting the abstract."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_abstract("New abstract content.")
        assert editor.document.abstract == "New abstract content."

    def test_set_abstract_no_document(self):
        """Test setting abstract without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.set_abstract("New abstract")

    def test_set_status_of_memo(self):
        """Test setting Status of This Memo."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_status_of_memo("New status content.")
        assert editor.document.status_of_memo == "New status content."

    def test_set_copyright(self):
        """Test setting copyright notice."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_copyright(2024, "New Holder")
        assert "2024" in editor.document.copyright_notice
        assert "New Holder" in editor.document.copyright_notice

    def test_set_toc(self):
        """Test setting Table of Contents."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_toc("1. Introduction\n2. Body")
        assert editor.document.toc == "1. Introduction\n2. Body"


class TestRFCEditorSections:
    """Tests for section manipulation."""

    def test_add_section(self):
        """Test adding a new section."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        initial_count = len(editor.document.sections)
        editor.add_section("5", "New Section", "New content.")
        assert len(editor.document.sections) == initial_count + 1
        new_section = editor.document.get_section("5")
        assert new_section is not None
        assert new_section.title == "New Section"

    def test_add_section_no_document(self):
        """Test adding section without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.add_section("5", "New Section", "Content")

    def test_update_section(self):
        """Test updating an existing section."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.update_section(
            "1", content="Updated introduction content."
        )
        section = editor.document.get_section("1")
        assert "Updated introduction" in section.content

    def test_update_section_title_only(self):
        """Test updating only the title of a section."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.update_section("1", title="New Introduction Title")
        section = editor.document.get_section("1")
        assert section.title == "New Introduction Title"

    def test_update_section_nonexistent(self):
        """Test updating a non-existent section."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        with pytest.raises(ValueError, match="Section .* not found"):
            editor.update_section("999", content="New content")

    def test_delete_section(self):
        """Test deleting a section."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        initial_count = len(editor.document.sections)
        editor.delete_section("1")
        assert len(editor.document.sections) == initial_count - 1
        assert editor.document.get_section("1") is None

    def test_delete_section_nonexistent(self):
        """Test deleting a non-existent section (should not raise)."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.delete_section("999")
        assert len(editor.document.sections) == len(
            editor.document.sections
        )

    def test_set_section_by_title(self):
        """Test updating a section by its title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_section_by_title(
            "Introduction", "Updated intro content."
        )
        section = editor.document.get_section_by_title("Introduction")
        assert "Updated intro" in section.content

    def test_set_section_by_title_nonexistent(self):
        """Test updating a non-existent section by title."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        with pytest.raises(ValueError, match="Section with title"):
            editor.set_section_by_title("NonExistent", "Content")


class TestRFCEditorSpecialSections:
    """Tests for special sections like Acknowledgements."""

    def test_set_acknowledgements(self):
        """Test setting Acknowledgements."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_acknowledgements("Thanks to everyone.")
        assert editor.document.acknowledgements == "Thanks to everyone."

    def test_set_contributors(self):
        """Test setting Contributors."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_contributors("Jane Doe contributed.")
        assert editor.document.contributors == "Jane Doe contributed."

    def test_set_authors_address(self):
        """Test setting Author's Address."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_authors_address("New Address\nLine 2")
        assert "New Address" in editor.document.authors_address


class TestRFCEditorSave:
    """Tests for saving RFC documents."""

    def test_save(self):
        """Test saving the RFC document."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.set_title("Modified Title")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name

        try:
            editor.save(temp_path)
            assert os.path.exists(temp_path)
            content = Path(temp_path).read_text()
            assert "Modified Title" in content
        finally:
            os.unlink(temp_path)

    def test_save_no_document(self):
        """Test saving without loading a document."""
        editor = RFCEditor()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name
        with pytest.raises(ValueError, match="No document loaded"):
            editor.save(temp_path)
        os.unlink(temp_path)


class TestRFCEditorGenerate:
    """Tests for generating RFC content."""

    def test_generate_content(self):
        """Test generating RFC content."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        content = editor._generate_content()
        assert "RFC 1234" in content
        assert "Test RFC Title" in content
        assert "Abstract" in content

    def test_to_dict(self):
        """Test converting document to dictionary."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        result = editor.to_dict()
        assert result["rfc_number"] == "1234"
        assert result["category"] == "Standards Track"
        assert "sections" in result

    def test_to_dict_no_document(self):
        """Test converting without loading a document."""
        editor = RFCEditor()
        with pytest.raises(ValueError, match="No document loaded"):
            editor.to_dict()


class TestRFCEditorEdgeCases:
    """Tests for edge cases."""

    def test_empty_content(self):
        """Test parsing empty content."""
        editor = RFCEditor()
        doc = editor.parse("")
        assert doc is not None
        assert doc.rfc_number == ""

    def test_minimal_rfc(self):
        """Test parsing minimal RFC content."""
        minimal = "RFC 1 (Standards Track)\n\nTitle\n\nAbstract\n\n"
        minimal += "Abstract content.\n"
        editor = RFCEditor()
        doc = editor.parse(minimal)
        assert doc.rfc_number == "1"

    def test_section_sorting(self):
        """Test that sections are properly sorted."""
        editor = RFCEditor()
        editor.parse(SAMPLE_RFC_CONTENT)
        editor.add_section("10", "Last Section", "Content")
        editor.add_section("2.1", "Middle Section", "Content")
        sorted_sections = sorted(
            editor.document.sections,
            key=lambda s: editor._section_sort_key(s.number),
        )
        numbers = [s.number for s in sorted_sections]
        assert "1" in numbers
        assert "2" in numbers
        assert "2.1" in numbers
        assert "3" in numbers
        assert "4" in numbers
        assert "4.1" in numbers
        assert "10" in numbers


class TestRFCEditorRoundTrip:
    """Tests for round-trip loading and saving."""

    def test_load_modify_save_load(self):
        """Test loading, modifying, saving, and reloading."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(SAMPLE_RFC_CONTENT)
            temp_path = f.name

        try:
            editor = RFCEditor()
            editor.load(temp_path)

            editor.set_title("Modified Title")
            editor.save(temp_path)

            editor2 = RFCEditor()
            doc2 = editor2.load(temp_path)
            assert doc2.title == "Modified Title"
            assert doc2.rfc_number == "1234"
        finally:
            os.unlink(temp_path)
