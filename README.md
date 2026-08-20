# Personal Planck-Style 4x10 Vial Keymap

This repository contains a reusable Vial layout backup for a 40-key
ortholinear keyboard with four rows of ten keys.

## What you get

The default typing layer is QWERTY, with Colemak available as an alternative.
Dedicated layers provide numbers and symbols, function and numpad keys, media
and navigation controls, and programming symbols.

The bottom row stays consistent across the typing layers:

```text
GUI  Alt  Shift  Control  Space  |  Backspace  Enter  Esc / Layer 4  Tab  Delete
```

Tapping `Esc / Layer 4` sends `Escape`. Holding it activates the layer
selector.

## Layers

| Layer | Purpose | Contents |
|------:|---------|----------|
| 0 | QWERTY | Standard QWERTY letters and punctuation |
| 1 | Numbers and symbols | Digits, shifted symbols, brackets, braces, backtick, tilde, slash, and backslash |
| 2 | Function and numpad | `F1`-`F12`, numpad keys, Insert, and Print Screen |
| 3 | Media and navigation | Mute, volume, brightness, Home, End, Insert, Delete, Page Up, Page Down, Print Screen, Scroll Lock, and programming symbols tuned for a Latin American host layout |
| 4 | Layer selector | Selects layers 0-5 with `DF(0)` through `DF(5)` |
| 5 | Colemak | Standard Colemak letters with the same punctuation and bottom row as QWERTY |
| 6-15 | Unused | Reserved layers |

The two typing layouts are:

```text
QWERTY                Colemak
Q W E R T Y U I O P   Q W F P G J L U Y ;
A S D F G H J K L ;   A R S T D H N E I O
Z X C V B N M , . /   Z X C V B K M , . /
```

## Switching layers

Hold the eighth key on the bottom row, `Esc / Layer 4`, then press one of the
first three keys on the left:

```text
Top row:   Layer 0  Layer 1  Layer 2
Home row:  Layer 3  Layer 4  Layer 5
```

The same selectors are repeated on the final three keys of those rows.
Selecting a layer with `DF(n)` makes it the active default layer. Use the same
sequence to switch again.

## Loading the keymap

The complete Vial backup is stored in [`keymap.vil`](keymap.vil).

1. Connect a keyboard running compatible Vial firmware.
2. Open [Vial](https://get.vial.today/).
3. Select **File > Load saved layout** and choose `keymap.vil`.

Vial applies key changes directly to the keyboard. Use **File > Save current
layout** to create a new backup after making changes.

The backup is tied to the keyboard definition and Vial UID used when it was
exported. It does not contain firmware and cannot configure unrelated hardware.
