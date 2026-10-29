import sys
sys.stdout.reconfigure(encoding='utf-8')

import re
from pathlib import Path
from urllib.parse import unquote

# EXACT delimiter: 73 "=" + "DIV80=="
SECTION_DELIMITER = "=" * 73 + "DIV80=="

def is_stone_line(text):
    return text.casefold().startswith("===stone:")

def validate_photo_path(
    photo_text, line_number, section_number, errors, base_directory
):
    photo_path = photo_text.split()[0]
    if not photo_path.startswith("file://./"):
        errors.append(
            f"[Section {section_number} @ line {line_number}] "
            f"Image path must start with file://./: {photo_text}"
        )
        return

    relative_path = unquote(photo_path.removeprefix("file://./"))
    resolved_path = base_directory / relative_path
    if not resolved_path.is_file():
        errors.append(
            f"[Section {section_number} @ line {line_number}] "
            f"Image file does not exist: {photo_path}"
        )

def validate_photo_paths(lines, section_number, errors, base_directory):
    for index, (line_number, text) in enumerate(lines):
        if not text.startswith("===Photos:"):
            continue

        photo_text = text.split(":", 1)[1].strip()
        if photo_text:
            validate_photo_path(photo_text, line_number, section_number, errors, base_directory)

        next_index = index + 1
        while next_index < len(lines) and not lines[next_index][1].startswith("==="):
            photo_line_number, photo_text = lines[next_index]
            photo_text = photo_text.strip()
            if photo_text:
                validate_photo_path(photo_text, photo_line_number, section_number, errors, base_directory)
            next_index += 1

def validate_section(
    lines, section_number, start_line_number, errors, warnings, base_directory
):
    """
    lines = list of (line_number, text)
    """

    if lines and lines[0][1].startswith("===PID: IGNORE_SECTION"):
        return

    # --- Structural header validation ---
    if len(lines) < 5:
        errors.append(f"[Section {section_number} @ line {start_line_number}] Section too short to contain required headers")
        return

    pid_line     = lines[0][1]
    coord_line   = lines[1][1]
    place_line   = lines[2][1]
    inscription_line = lines[3][1]
    stones_line  = lines[4][1]

    # Rule 1: PID line
    if not pid_line.startswith("===PID:"):
        errors.append(f"[Section {section_number} @ line {lines[0][0]}] Missing or malformed PID line")
        return

    # Rule 2: Coord line
    if not coord_line.startswith("===Coord:"):
        errors.append(f"[Section {section_number} @ line {lines[1][0]}] Missing or malformed Coord line")
        return

    # Rule 3: Place line
    if not place_line.startswith("===Place:"):
        errors.append(f"[Section {section_number} @ line {lines[2][0]}] Missing or malformed Place line")
        return

    # Rule 4: Inscription-name line
    if not inscription_line.startswith("===Inscription-name:"):
        errors.append(
            f"[Section {section_number} @ line {lines[3][0]}] "
            "Missing or malformed Inscription-name line"
        )
        return

    if not inscription_line.split(":", 1)[1].strip():
        warnings.append(
            f"[Section {section_number} @ line {lines[3][0]}] "
            "===Inscription-name: has no name on the same line"
        )

    # Rule 5: Stones line
    if not stones_line.startswith("===Stones:"):
        errors.append(f"[Section {section_number} @ line {lines[4][0]}] Missing or malformed Stones line")
        return

    validate_photo_paths(lines, section_number, errors, base_directory)

    # Stones value must be integer >=1 or integer-V or 0-V
    m = re.match(r"^===Stones:\s*(?:0-V|[1-9]\d*(?:-V)?)$", stones_line)
    if not m:
        errors.append(
            f"[Section {section_number} @ line {lines[3][0]}] Stones value must be integer or integer-V, with 0-V as the only zero-stone form: {stones_line}"
        )
        return

    # Extract stones_value and vacant_flag
    stones_raw = stones_line.split(":", 1)[1].strip()
    vacant_flag = stones_raw.endswith("-V")

    if stones_raw == "0-V":
        stones_value = 0
    else:
        stones_value = int(stones_raw.replace("-V", ""))

    # --- Collect stone blocks ---
    stone_blocks = []
    numbered_stones = []

    for ln, text in lines:
        if is_stone_line(text):
            stone_blocks.append((ln, text))
            m2 = re.match(r"^===Stone:\s*([1-9]\d*)$", text)
            if m2:
                numbered_stones.append((ln, int(m2.group(1))))
            elif text.strip() in {"===Stone: VACANT", "===Stone: _NOT-A-PLOT"}:
                pass
            else:
                errors.append(f"[Section {section_number} @ line {ln}] Invalid Stone line: {text}")

    stone_count = len(stone_blocks)
    numbered_count = len(numbered_stones)

    # --- Stones = 0-V case ---
    if stones_value == 0:
        vacant_markers = {"===Stone: VACANT", "===Stone: _NOT-A-PLOT"}
        if stone_count != 1 or not any(
            text.strip() in vacant_markers for _, text in stone_blocks
        ):
            errors.append(
                f"[Section {section_number} @ line {start_line_number}] "
                "Stones=0-V section must contain exactly one "
                "===Stone: VACANT or ===Stone: _NOT-A-PLOT line"
            )

        # Must contain one or more dated-entry sets (Date/Photos/Notes, each optional)
        found_sets = False
        i = 0
        while i < len(lines):
            ln, text = lines[i]
            if text.startswith("===Date:") or text.startswith("===Photos:") or text.startswith("===Notes:"):
                found_sets = True
                while i < len(lines) and (
                    lines[i][1].startswith("===Date:") or
                    lines[i][1].startswith("===Photos:") or
                    lines[i][1].startswith("===Notes:")
                ):
                    i += 1
                continue
            i += 1

        if not found_sets:
            errors.append(
                f"[Section {section_number} @ line {start_line_number}] Stones=0-V section must contain at least one dated-entry set (Date/Photos/Notes)"
            )
        return

    # --- Stones >=1 case ---
    expected_numbered = stones_value
    if numbered_count != expected_numbered:
        errors.append(
            f"[Section {section_number} @ line {lines[3][0]}] Numbered stone count mismatch: expected {expected_numbered}, found {numbered_count}"
        )

    # Validate stone numbering consecutive and decreasing
    nums = [n for ln, n in numbered_stones]
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1] - 1:
            errors.append(
                f"[Section {section_number} @ line {numbered_stones[i][0]}] Stone numbers must decrease consecutively: {nums}"
            )
            break

    if nums and nums[0] != expected_numbered:
        errors.append(
            f"[Section {section_number} @ line {lines[3][0]}] Stones value {expected_numbered} does not match largest stone number {nums[0]}"
        )

    # Validate each numbered stone has Date + Transcription + transcription block + dated-entry sets
    for ln, text in stone_blocks:
        mstone = re.match(r"^===Stone:\s*([1-9]\d*)$", text)
        if not mstone:
            continue

        idx = None
        for i, (lno, t) in enumerate(lines):
            if lno == ln:
                idx = i
                break

        if idx is None or idx + 2 >= len(lines):
            errors.append(f"[Section {section_number} @ line {ln}] Stone block incomplete; missing Date/Transcription")
            continue

        date_line = lines[idx+1][1]
        trans_line = lines[idx+2][1]

        if not date_line.startswith("===Date:"):
            errors.append(
                f"[Section {section_number} @ line {lines[idx+1][0]}] Stone must have ===Date: immediately after ===Stone:"
            )

        if not trans_line.startswith("===Transcription:"):
            errors.append(
                f"[Section {section_number} @ line {lines[idx+2][0]}] Stone must have ===Transcription: immediately after ===Date:"
            )

        # Validate transcription block markers
        begin_idx = idx+3
        if begin_idx >= len(lines):
            errors.append(
                f"[Section {section_number} @ line {lines[idx+2][0]}] Transcription block missing begin marker"
            )
            continue

        begin_line_no, begin_text = lines[begin_idx]
        if begin_text != "---------------------------------------------begin---DIV60--":
            errors.append(
                f"[Section {section_number} @ line {begin_line_no}] Transcription block must start with exact begin marker"
            )
            continue

        end_idx = None
        for j in range(begin_idx+1, len(lines)):
            if lines[j][1] == "---------------------------------------------end-----DIV60--":
                end_idx = j
                break

        if end_idx is None:
            errors.append(
                f"[Section {section_number} @ line {begin_line_no}] Transcription block missing end marker"
            )
            continue

        if end_idx == begin_idx+1:
            errors.append(
                f"[Section {section_number} @ line {begin_line_no}] Transcription block must contain at least one line of text"
            )
            continue

        text_lines = [lines[k][1].strip() for k in range(begin_idx+1, end_idx)]
        if all(t == "" for t in text_lines):
            errors.append(
                f"[Section {section_number} @ line {begin_line_no}] Transcription block cannot be empty or whitespace-only"
            )
            continue

        # Validate at least one dated-entry set after transcription
        found_set = False
        j = end_idx + 1

        while j < len(lines):
            if is_stone_line(lines[j][1]):
                break

            # Look for ===Date: with immediate ===Photos:
            if lines[j][1].startswith("===Date:"):
                if j + 1 < len(lines) and lines[j+1][1].startswith("===Photos:"):
                    # Now search for ===Notes: after Photos until next Date or Stone
                    k = j + 2
                    while k < len(lines):
                        if is_stone_line(lines[k][1]):
                            break
                        if lines[k][1].startswith("===Date:"):
                            break
                        if lines[k][1].startswith("===Notes:"):
                            found_set = True
                            break
                        k += 1
                    if found_set:
                        break
            j += 1

        if not found_set:
            errors.append(
                f"[Section {section_number} @ line {ln}] Numbered stone must contain at least one dated-entry set (===Date:, ===Photos:, ===Notes:)"
            )

    # After all stones, require Interpretation/Location/Table/Status
    required = ["===Interpretation:", "===Location:", "===Table:", "===Status:"]
    req_idx = 0
    for j in range(len(lines)):
        if lines[j][1].startswith(required[req_idx]):
            req_idx += 1
            if req_idx == len(required):
                break

    if req_idx != len(required):
        errors.append(
            f"[Section {section_number} @ line {start_line_number}] Missing required post-stone block: Interpretation/Location/Table/Status"
        )


def validate_file(path):
    errors = []
    warnings = []

    with open(path, "r", encoding="utf-8") as f:
        lines = [(i+1, line.rstrip("\n")) for i, line in enumerate(f)]

    sections = []
    current = []

    for ln, text in lines:

        # Corrupted delimiter detection
        if text.startswith("=") and "DIV80==" in text and text != SECTION_DELIMITER:
            errors.append(f"[Line {ln}] Corrupted delimiter: {text}")

        # Valid delimiter
        if text == SECTION_DELIMITER:
            if current:
                sections.append(current)
            current = []
            continue

        current.append((ln, text))

    if current:
        sections.append(current)

    # Validate each section
    for idx, sec in enumerate(sections, start=1):
        start_ln = sec[0][0]
        validate_section(sec, idx, start_ln, errors, warnings, Path(path).resolve().parent)

    # Output
    if errors:
        print("Validation errors:")
        for e in errors:
            print(e)
    else:
        print("No validation errors found.")

    if warnings:
        print("Validation warnings:")
        for warning in warnings:
            print(warning)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validator.py <cemetery_file.txt>")
        sys.exit(1)

    validate_file(sys.argv[1])
