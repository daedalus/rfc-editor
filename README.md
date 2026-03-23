# RFC Editor Library

A Python library for parsing and editing RFC (Request for Comments) TXT documents.

## Features

- Parse RFC TXT documents and extract all sections
- Edit all RFC document sections including:
  - Title
  - Abstract
  - Status of This Memo
  - Copyright Notice
  - Table of Contents
  - Numbered sections (1., 2., etc.)
  - Acknowledgements
  - Contributors
  - Author's Address
- Add, update, and delete sections
- Save modified documents back to TXT format

## Installation

```bash
pip install rfc-editor
```

Or install from source:

```bash
pip install -e .
```

## Usage

### Parse an RFC Document

```python
from rfc_editor import RFCEditor

editor = RFCEditor()
doc = editor.load("rfc1234.txt")

# Or parse from string
doc = editor.parse(rfc_content_string)
```

### Access Document Sections

```python
print(doc.rfc_number)  # RFC number
print(doc.category)   # e.g., "Standards Track"
print(doc.title)      # RFC title
print(doc.abstract)  # Abstract content
```

### Query Sections

```python
# Get title
title = editor.get_title()

# Get abstract
abstract = editor.get_abstract()

# Get status of this memo
status = editor.get_status_of_memo()

# Get copyright (returns tuple of year and holders)
year, holders = editor.get_copyright()

# Get table of contents
toc = editor.get_toc()

# Get acknowledgements
acknowledgements = editor.get_acknowledgements()

# Get contributors
contributors = editor.get_contributors()

# Get author's address
address = editor.get_authors_address()

# Get section by title (returns RFCSection or None)
section = editor.get_section_by_title("Introduction")
```

### Edit Sections

```python
# Edit title
editor.set_title("New Title")

# Edit abstract
editor.set_abstract("New abstract content...")

# Edit status
editor.set_status_of_memo("New status content...")

# Edit copyright
editor.set_copyright(2024, "Example Corp")

# Edit TOC
editor.set_toc("1. Introduction\n2. Body")

# Update a numbered section
editor.update_section("1", content="Updated introduction content...")

# Add a new section
editor.add_section("5", "New Section", "Section content...")

# Delete a section
editor.delete_section("1")

# Edit by section title
editor.set_section_by_title("Introduction", "New content...")
```

### Save the Document

```python
editor.save("output.txt")
```

### Convert to Dictionary

```python
data = editor.to_dict()
print(data["title"])
print(data["sections"])
```

## Development

### Install Dev Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Run Linting

```bash
flake8 src/ tests/
ruff check src/ tests/
black --check src/ tests/
```

## Project Structure

```
rfc-editor/
├── src/
│   └── rfc_editor/
│       └── __init__.py    # Main library code
├── tests/
│   ├── test_author.py
│   ├── test_document.py
│   ├── test_editor.py
│   └── test_section.py
├── pyproject.toml
├── README.md
├── .gitignore
└── SPEC.md
```

## Version

0.1.0.1

## License

MIT
