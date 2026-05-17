"""Chinese text style conversion (simplified/traditional)."""

from __future__ import annotations

import opencc

_converter_s2t = opencc.OpenCC("s2t")
_converter_t2s = opencc.OpenCC("t2s")


def to_simplified(text: str | None) -> str | None:
    """Convert traditional Chinese to simplified Chinese."""
    if text is None:
        return None
    return _converter_t2s.convert(text)


def to_traditional(text: str | None) -> str | None:
    """Convert simplified Chinese to traditional Chinese."""
    if text is None:
        return None
    return _converter_s2t.convert(text)