"""RFC Editor Library - Parse and edit RFC TXT documents."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RFCAuthor:
    """Represents an RFC author."""

    name: str = ""
    organization: str = ""
    email: str = ""
    address: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "organization": self.organization,
            "email": self.email,
            "address": self.address,
        }


@dataclass
class RFCSection:
    """Represents a section in an RFC document."""

    number: str = ""
    title: str = ""
    content: str = ""

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "title": self.title,
            "content": self.content,
        }


@dataclass
class RFCDocument:
    """Represents a complete RFC document."""

    rfc_number: str = ""
    category: str = ""
    title: str = ""
    abstract: str = ""
    authors: list[RFCAuthor] = field(default_factory=list)
    status_of_memo: str = ""
    copyright_notice: str = ""
    toc: str = ""
    sections: list[RFCSection] = field(default_factory=list)
    acknowledgements: str = ""
    contributors: str = ""
    index: str = ""
    authors_address: str = ""
    raw_content: str = ""

    def get_section(self, number: str) -> RFCSection | None:
        """Get a section by number."""
        for section in self.sections:
            if section.number == number:
                return section
        return None

    def get_section_by_title(self, title: str) -> RFCSection | None:
        """Get a section by title (case-insensitive partial match)."""
        title_lower = title.lower()
        for section in self.sections:
            if title_lower in section.title.lower():
                return section
        return None


class RFCEditor:
    """Editor for RFC TXT documents."""

    def __init__(self):
        """Initialize the RFC editor."""
        self.document: RFCDocument | None = None

    def load(self, filepath: str | Path) -> RFCDocument:
        """Load an RFC TXT file and parse its sections."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        content = path.read_text(encoding="utf-8")
        return self.parse(content)

    def parse(self, content: str) -> RFCDocument:
        """Parse RFC content and return an RFCDocument object."""
        doc = RFCDocument(raw_content=content)
        lines = content.split("\n")

        self._parse_header(lines, doc)
        self._parse_title(lines, doc)
        doc.abstract = self._extract_section(lines, "Abstract")
        doc.status_of_memo = self._extract_section(
            lines, "Status of This Memo"
        )
        doc.copyright_notice = self._extract_copyright(lines)
        doc.toc = self._extract_section(lines, "Table of Contents")
        self._parse_sections(lines, doc)
        doc.acknowledgements = self._extract_section(
            lines, "Acknowledgements"
        )
        doc.contributors = self._extract_section(lines, "Contributors")
        doc.index = self._extract_section(lines, "Index")
        doc.authors_address = self._extract_section(
            lines, "Author's Address"
        )

        self.document = doc
        return doc

    def _parse_header(self, lines: list[str], doc: RFCDocument) -> None:
        """Parse the RFC header line."""
        header_pattern = re.compile(r"^RFC\s+(\d+)\s+\((.+)\)$")
        for line in lines:
            match = header_pattern.match(line.strip())
            if match:
                doc.rfc_number = match.group(1)
                doc.category = match.group(2)
                return

    def _parse_title(self, lines: list[str], doc: RFCDocument) -> None:
        """Parse the RFC title."""
        for line in lines:
            line_stripped = line.strip()
            if (
                line_stripped
                and not line_stripped.startswith("RFC")
                and line_stripped != "Abstract"
            ):
                doc.title = line_stripped
                return

    def _extract_section(
        self, lines: list[str], section_name: str
    ) -> str:
        """Extract a section by name."""
        content = []
        found_section = False
        started = False

        for line in lines:
            stripped = line.strip()
            if stripped == section_name:
                found_section = True
                started = False
                continue

            if found_section:
                if not stripped and not started:
                    continue
                started = True
                if not stripped:
                    break
                content.append(line.rstrip())

        return "\n".join(content).strip()

    def _extract_copyright(self, lines: list[str]) -> str:
        """Extract the Copyright notice."""
        content = []
        in_copyright = False

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("Copyright"):
                in_copyright = True

            if in_copyright:
                content.append(line_stripped)
                if not line and content:
                    break
                if (
                    not line_stripped.startswith("Copyright")
                    and line_stripped
                ):
                    break

        return "\n".join(content).strip()

    def _parse_sections(
        self, lines: list[str], doc: RFCDocument
    ) -> None:
        """Parse numbered sections."""
        section_pattern = re.compile(
            r"^(\d+(?:\.\d+)*)\.\s+([A-Za-z].+)$"
        )

        for i, line in enumerate(lines):
            match = section_pattern.match(line.strip())
            if match:
                title = match.group(2).strip()
                if "................................" in title:
                    continue

                section = RFCSection(
                    number=match.group(1),
                    title=title,
                )

                content_lines = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line:
                        break
                    if section_pattern.match(next_line):
                        if (
                            "................................"
                            in next_line
                        ):
                            j += 1
                            continue
                        break
                    if next_line in [
                        "Abstract",
                        "Status of This Memo",
                        "Table of Contents",
                        "Acknowledgements",
                        "Contributors",
                        "Index",
                        "Author's Address",
                    ]:
                        break
                    content_lines.append(lines[j].rstrip())
                    j += 1

                section.content = "\n".join(content_lines).strip()
                doc.sections.append(section)

    def set_title(self, title: str) -> None:
        """Set the RFC title."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.title = title

    def set_abstract(self, abstract: str) -> None:
        """Set the RFC abstract."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.abstract = abstract

    def set_status_of_memo(self, status: str) -> None:
        """Set the Status of This Memo section."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.status_of_memo = status

    def set_copyright(self, year: int, holders: str) -> None:
        """Set the copyright notice."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.copyright_notice = (
            f"Copyright (c) {year} {holders}"
        )

    def set_toc(self, toc: str) -> None:
        """Set the Table of Contents."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.toc = toc

    def add_section(
        self, number: str, title: str, content: str
    ) -> None:
        """Add a new section to the document."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.sections.append(
            RFCSection(number=number, title=title, content=content)
        )
        self.document.sections.sort(
            key=lambda s: self._section_sort_key(s.number)
        )

    def update_section(
        self,
        number: str,
        title: str | None = None,
        content: str | None = None,
    ) -> None:
        """Update an existing section by number."""
        if self.document is None:
            raise ValueError("No document loaded")
        section = self.document.get_section(number)
        if section is None:
            raise ValueError(f"Section {number} not found")
        if title is not None:
            section.title = title
        if content is not None:
            section.content = content

    def delete_section(self, number: str) -> None:
        """Delete a section by number."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.sections = [
            s for s in self.document.sections if s.number != number
        ]

    def set_acknowledgements(self, content: str) -> None:
        """Set the Acknowledgements section."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.acknowledgements = content

    def set_contributors(self, content: str) -> None:
        """Set the Contributors section."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.contributors = content

    def set_authors_address(self, address: str) -> None:
        """Set the Author's Address section."""
        if self.document is None:
            raise ValueError("No document loaded")
        self.document.authors_address = address

    def set_section_by_title(self, title: str, content: str) -> None:
        """Update a section by its title."""
        if self.document is None:
            raise ValueError("No document loaded")
        section = self.document.get_section_by_title(title)
        if section is None:
            raise ValueError(f"Section with title '{title}' not found")
        section.content = content

    def _section_sort_key(self, number: str) -> tuple:
        """Generate a sort key for section numbers."""
        parts = number.split(".")
        return tuple(int(p) if p.isdigit() else 0 for p in parts)

    def save(self, filepath: str | Path) -> None:
        """Save the RFC document to a TXT file."""
        if self.document is None:
            raise ValueError("No document loaded")

        path = Path(filepath)
        content = self._generate_content()
        path.write_text(content, encoding="utf-8")

    def _generate_content(self) -> str:
        """Generate the RFC TXT content from the document."""
        if self.document is None:
            raise ValueError("No document loaded")

        doc = self.document
        lines = []

        if doc.rfc_number:
            lines.append(f"RFC {doc.rfc_number} ({doc.category})")
        lines.append("")
        lines.append(doc.title)
        lines.append("")
        lines.append("Abstract")
        lines.append("")
        lines.append(doc.abstract)
        lines.append("")
        lines.append("Status of This Memo")
        lines.append("")
        lines.append(doc.status_of_memo)
        lines.append("")
        lines.append(doc.copyright_notice)
        lines.append("")
        lines.append("Table of Contents")
        lines.append("")
        lines.append(doc.toc)
        lines.append("")

        for section in sorted(
            doc.sections, key=lambda s: self._section_sort_key(s.number)
        ):
            lines.append(f"{section.number}. {section.title}")
            lines.append("")
            lines.append(section.content)
            lines.append("")

        if doc.acknowledgements:
            lines.append("Acknowledgements")
            lines.append("")
            lines.append(doc.acknowledgements)
            lines.append("")

        if doc.contributors:
            lines.append("Contributors")
            lines.append("")
            lines.append(doc.contributors)
            lines.append("")

        if doc.index:
            lines.append("Index")
            lines.append("")
            lines.append(doc.index)
            lines.append("")

        if doc.authors_address:
            lines.append("Author's Address")
            lines.append("")
            lines.append(doc.authors_address)
            lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Convert the document to a dictionary."""
        if self.document is None:
            raise ValueError("No document loaded")
        return {
            "rfc_number": self.document.rfc_number,
            "category": self.document.category,
            "title": self.document.title,
            "abstract": self.document.abstract,
            "status_of_memo": self.document.status_of_memo,
            "copyright_notice": self.document.copyright_notice,
            "toc": self.document.toc,
            "sections": [s.to_dict() for s in self.document.sections],
            "acknowledgements": self.document.acknowledgements,
            "contributors": self.document.contributors,
            "index": self.document.index,
            "authors_address": self.document.authors_address,
        }
