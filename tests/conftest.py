"""Test fixtures for RFC Editor tests."""

import pytest

from rfc_editor import RFCEditor


@pytest.fixture
def sample_rfc_content():
    """Sample RFC content for testing."""
    return """RFC 1234 (Standards Track)

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

Author's Address

John Doe
Example Corp
123 Main Street
City, State 12345
Email: john@example.com
"""


@pytest.fixture
def editor_with_sample():
    """RFCEditor instance loaded with sample content."""
    editor = RFCEditor()
    editor.parse(sample_rfc_content())
    return editor
