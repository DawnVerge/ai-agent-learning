"""JSON extraction used by the intent recognition teaching project."""

import json


def extract_json_object(text: str | None) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {}
    decoder = json.JSONDecoder()
    for index, character in enumerate(text):
        if character != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return {}
