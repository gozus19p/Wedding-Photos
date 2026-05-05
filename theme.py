from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

TITLE_FONT_FAMILY = "Boheme Floral"


@lru_cache(maxsize=1)
def title_font_face_css() -> str:
    font_path = Path(__file__).resolve().parent / "pages" / "Boheme Floral.ttf"
    encoded_font = base64.b64encode(font_path.read_bytes()).decode("ascii")
    return (
        "@font-face {"
        f"font-family: '{TITLE_FONT_FAMILY}';"
        "src: url(data:font/ttf;base64,"
        f"{encoded_font}"
        ") format('truetype');"
        "font-weight: normal;"
        "font-style: normal;"
        "font-display: swap;"
        "}"
    )
