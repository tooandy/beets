"""Chinese text style conversion (simplified/traditional)."""

from __future__ import annotations

import json
from typing import Any

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


def convert_dict(data: Any, converter=to_simplified) -> Any:
    """Recursively convert all string values in a dict/list structure.

    Args:
        data: The data structure to convert (dict, list, or string)
        converter: Conversion function to use (default: to_simplified)

    Returns:
        The converted data structure with all strings converted.
    """
    if isinstance(data, str):
        return converter(data)

    # Serialize to JSON, convert the string, then parse back
    json_str = json.dumps(data, ensure_ascii=False)
    converted_str = converter(json_str)
    return json.loads(converted_str)