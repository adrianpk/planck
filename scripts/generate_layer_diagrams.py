#!/usr/bin/env python3
"""Generate Planck-style layer reference SVG files from the Vial backup."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEYMAP_PATH = ROOT / "keymap.vil"
OUTPUT_DIR = ROOT / "assets" / "img" / "layers"

LAYER_METADATA = {
    0: {
        "slug": "qwerty",
        "title": "QWERTY",
        "summary": "QWERTY typing layer",
        "legend": [
            ("primary", "Letters"),
            ("symbol", "Punctuation"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
    1: {
        "slug": "numbers-symbols",
        "title": "NUMBERS & SYMBOLS",
        "summary": "Numbers and symbols layer",
        "legend": [
            ("primary", "Numbers"),
            ("symbol", "Symbols"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
    2: {
        "slug": "function-numpad",
        "title": "FUNCTION & NUMPAD",
        "summary": "Function and numpad layer",
        "legend": [
            ("primary", "Function keys"),
            ("secondary", "Numpad"),
            ("action", "System keys"),
            ("modifier", "Modifiers"),
            ("layer", "Layer access"),
        ],
    },
    3: {
        "slug": "media-navigation",
        "title": "MEDIA & NAVIGATION",
        "summary": "Media, navigation, and programming symbols layer",
        "legend": [
            ("secondary", "Media"),
            ("action", "Navigation"),
            ("symbol", "Programming symbols"),
            ("modifier", "Modifiers"),
            ("layer", "Layer access"),
        ],
    },
    4: {
        "slug": "layer-selector",
        "title": "LAYER SELECTOR",
        "summary": "Default layer selector",
        "legend": [
            ("layer", "Layer selection"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("empty", "Unassigned"),
        ],
    },
    5: {
        "slug": "colemak",
        "title": "COLEMAK",
        "summary": "Colemak typing layer",
        "legend": [
            ("primary", "Letters"),
            ("symbol", "Punctuation"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
    6: {
        "slug": "extended-function-keys",
        "title": "EXTENDED FUNCTION KEYS",
        "summary": "Extended function keys for host-defined shortcuts",
        "legend": [
            ("primary", "Function keys"),
            ("empty", "Unassigned"),
        ],
    },
}

COLORS = {
    "primary": "#d1d5db",
    "symbol": "#c4b5d4",
    "modifier": "#aeb0ec",
    "action": "#acd0ed",
    "layer": "#fcf7a8",
    "secondary": "#b9dfc5",
    "empty": "#f3f4f6",
}

PHYSICAL_POSITIONS = (
    ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (4, 0), (4, 1), (4, 2)),
    ((1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (4, 3), (4, 4), (4, 5)),
    ((2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (4, 6), (5, 0), (5, 1)),
    ((3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (5, 2), (5, 3), (5, 4)),
)

KEY_WIDTH = 58
KEY_HEIGHT = 54
COLUMN_STEP = 68
ROW_STEP = 64
LEFT_X = 220
TOP_Y = 112

SIMPLE_LABELS = {
    "KC_0": "0",
    "KC_1": "1",
    "KC_2": "2",
    "KC_3": "3",
    "KC_4": "4",
    "KC_5": "5",
    "KC_6": "6",
    "KC_7": "7",
    "KC_8": "8",
    "KC_9": "9",
    "KC_MINUS": "−",
    "KC_EQUAL": "=",
    "KC_LBRACKET": "[",
    "KC_RBRACKET": "]",
    "KC_GRAVE": "`",
    "KC_BSLASH": "\\",
    "KC_SLASH": "/",
    "KC_SCOLON": ";",
    "KC_COMMA": ",",
    "KC_DOT": ".",
    "KC_INSERT": "Ins",
    "KC_DELETE": "Del",
    "KC_HOME": "Home",
    "KC_END": "End",
    "KC_PGUP": "PgUp",
    "KC_PGDOWN": "PgDn",
    "KC_PSCREEN": "PrtSc",
    "KC_SCROLLLOCK": "ScrLk",
    "KC_MUTE": "Mute",
    "KC_VOLD": "Vol −",
    "KC_VOLU": "Vol +",
    "KC_BRID": "Bright −",
    "KC_BRIU": "Bright +",
    "KC_NONUS_BSLASH": "< >",
}

BOTTOM_KEYS = {
    "KC_LGUI": ("GUI", "", "modifier"),
    "LSFT(KC_LGUI)": ("GUI", "SHIFT", "modifier"),
    "KC_LALT": ("Alt", "", "modifier"),
    "KC_LSHIFT": ("Shift", "", "modifier"),
    "KC_LCTRL": ("Ctrl", "", "modifier"),
    "KC_SPACE": ("Space", "", "action"),
    "LT6(KC_SPACE)": ("Space", "HOLD L6", "layer"),
    "KC_BSPACE": ("Bksp", "", "action"),
    "KC_ENTER": ("Enter", "", "action"),
    "KC_TAB": ("Tab", "", "action"),
    "KC_DELETE": ("Del", "", "action"),
    "LT4(KC_ESCAPE)": ("Esc", "HOLD L4", "layer"),
}

SHIFTED_SYMBOLS = {
    "LSFT(KC_1)": "!",
    "LSFT(KC_2)": "@",
    "LSFT(KC_3)": "#",
    "LSFT(KC_4)": "$",
    "LSFT(KC_5)": "%",
    "LSFT(KC_6)": "^",
    "LSFT(KC_7)": "&",
    "LSFT(KC_8)": "*",
    "LSFT(KC_9)": "(",
    "LSFT(KC_0)": ")",
    "LSFT(KC_LBRACKET)": "{",
    "LSFT(KC_RBRACKET)": "}",
    "LSFT(KC_GRAVE)": "~",
}

LATAM_SYMBOLS = {
    "LSFT(KC_8)": "(",
    "LSFT(KC_9)": ")",
    "RALT(KC_8)": "[",
    "RALT(KC_9)": "]",
    "RALT(KC_7)": "{",
    "RALT(KC_0)": "}",
    "KC_NONUS_BSLASH": "< >",
    "LSFT(KC_7)": "/",
    "RALT(KC_MINUS)": "\\",
    "RALT(KC_1)": "|",
    "RALT(KC_4)": "~",
    "KC_GRAVE": "|",
    "KC_LBRACKET": "´",
    "RALT(KC_6)": "¬",
}


def physical_layer(keymap: dict[str, object], layer_number: int) -> list[list[str]]:
    matrix = keymap["layout"][layer_number]
    return [
        [matrix[matrix_row][matrix_column] for matrix_row, matrix_column in physical_row]
        for physical_row in PHYSICAL_POSITIONS
    ]


def describe_keycode(keycode: str, layer: int) -> tuple[str, str, str]:
    if keycode in BOTTOM_KEYS:
        return BOTTOM_KEYS[keycode]

    default_layer = re.fullmatch(r"DF\((\d+)\)", keycode)
    if default_layer:
        return f"L{default_layer.group(1)}", "SELECT", "layer"

    if keycode in {"KC_NO", "KC_TRNS"}:
        return "—", "", "empty"

    letter = re.fullmatch(r"KC_([A-Z])", keycode)
    if letter:
        return letter.group(1), "", "primary"

    function_key = re.fullmatch(r"KC_F(\d+)", keycode)
    if function_key:
        return f"F{function_key.group(1)}", "", "primary"

    numpad_digit = re.fullmatch(r"KC_KP_(\d)", keycode)
    if numpad_digit:
        return numpad_digit.group(1), "NUM", "secondary"

    numpad_labels = {
        "KC_KP_SLASH": "/",
        "KC_KP_ASTERISK": "*",
        "KC_KP_MINUS": "−",
        "KC_KP_PLUS": "+",
        "KC_KP_EQUAL": "=",
        "KC_KP_DOT": ".",
    }
    if keycode in numpad_labels:
        return numpad_labels[keycode], "NUM", "secondary"

    if layer == 3 and keycode in LATAM_SYMBOLS:
        return LATAM_SYMBOLS[keycode], "", "symbol"

    if keycode in {"KC_MUTE", "KC_VOLD", "KC_VOLU", "KC_BRID", "KC_BRIU"}:
        return SIMPLE_LABELS[keycode], "", "secondary"

    if keycode in {
        "KC_INSERT",
        "KC_DELETE",
        "KC_HOME",
        "KC_END",
        "KC_PGUP",
        "KC_PGDOWN",
        "KC_PSCREEN",
        "KC_SCROLLLOCK",
    }:
        return SIMPLE_LABELS[keycode], "", "action"

    if keycode in SHIFTED_SYMBOLS:
        return SHIFTED_SYMBOLS[keycode], "", "symbol"

    if keycode in SIMPLE_LABELS:
        category = "primary" if keycode[3:].isdigit() else "symbol"
        return SIMPLE_LABELS[keycode], "", category

    return keycode.removeprefix("KC_"), "", "primary"


def key_svg(x: int, y: int, keycode: str, layer: int) -> str:
    label, sublabel, category = describe_keycode(keycode, layer)
    fill = COLORS[category]
    label_size = 17 if len(label) <= 5 else 12
    label_y = y + KEY_HEIGHT / 2 + (-4 if sublabel else 1)
    parts = [
        (
            f'<rect x="{x}" y="{y}" width="{KEY_WIDTH}" height="{KEY_HEIGHT}" '
            f'rx="8" fill="{fill}" stroke="#8b8f97" stroke-width="1.2"/>'
        ),
        (
            f'<text x="{x + KEY_WIDTH / 2}" y="{label_y}" class="key-label" '
            f'font-size="{label_size}">{escape(label)}</text>'
        ),
    ]
    if sublabel:
        parts.append(
            f'<text x="{x + KEY_WIDTH / 2}" y="{y + KEY_HEIGHT / 2 + 13}" '
            f'class="key-sub">{escape(sublabel)}</text>'
        )
    return "\n".join(parts)


def legend_svg(items: list[tuple[str, str]]) -> str:
    item_widths = [32 + len(label) * 7 for _, label in items]
    total_width = sum(item_widths) + 18 * (len(items) - 1)
    cursor = (1120 - total_width) / 2
    parts: list[str] = []

    for (category, label), width in zip(items, item_widths, strict=True):
        parts.append(
            f'<rect x="{cursor:.1f}" y="452" width="12" height="12" rx="3" '
            f'fill="{COLORS[category]}" stroke="#8b8f97" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{cursor + 19:.1f}" y="462" class="legend-label">{escape(label)}</text>'
        )
        cursor += width + 18

    return "\n".join(parts)


def generate_svg(layer_number: int, rows: list[list[str]]) -> str:
    metadata = LAYER_METADATA[layer_number]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 500" role="img"',
        f'  aria-labelledby="layer-{layer_number}-title layer-{layer_number}-description">',
        f'  <title id="layer-{layer_number}-title">Planck-style layer {layer_number}: {escape(metadata["title"])}</title>',
        f'  <desc id="layer-{layer_number}-description">{escape(metadata["summary"])}</desc>',
        "  <style>",
        '    text { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }',
        "    .kicker { font-size: 12px; font-weight: 600; letter-spacing: 2px; text-anchor: middle; fill: #718096; }",
        "    .title { font-size: 27px; font-weight: 600; text-anchor: middle; }",
        "    .key-label { font-weight: 500; text-anchor: middle; dominant-baseline: middle; }",
        "    .key-sub { font-size: 8px; font-weight: 600; letter-spacing: 0.4px; text-anchor: middle; fill: #667085; }",
        "    .legend-label { font-size: 11px; fill: #667085; }",
        "  </style>",
        '  <text x="560" y="28" class="kicker">PLANCK-STYLE · 4×10</text>',
        f'  <text x="560" y="66" class="title">LAYER {layer_number} · {escape(metadata["title"])}</text>',
    ]

    for row_number, row in enumerate(rows):
        for column_number, keycode in enumerate(row):
            parts.append(
                "  "
                + key_svg(
                    LEFT_X + column_number * COLUMN_STEP,
                    TOP_Y + row_number * ROW_STEP,
                    keycode,
                    layer_number,
                )
            )

    parts.extend(("  " + legend_svg(metadata["legend"]), "</svg>", ""))
    return "\n".join(parts)


def main() -> None:
    keymap = json.loads(KEYMAP_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for layer_number, metadata in LAYER_METADATA.items():
        output_path = OUTPUT_DIR / f"layer-{layer_number}-{metadata['slug']}.svg"
        output_path.write_text(
            generate_svg(layer_number, physical_layer(keymap, layer_number)),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
