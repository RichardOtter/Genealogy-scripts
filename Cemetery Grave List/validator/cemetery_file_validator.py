import sys
sys.stdout.reconfigure(encoding='utf-8')

import re

# EXACT delimiter: 73 "=" + "DIV80=="
SECTION_DELIMITER = "=" * 73 + "DIV80=="

def validate_section(lines, section_number, start_line_number, errors):
    """
    lines = list of (line_number, text)
    """

    # --- Find ===Stones: line ---
    stones_line = None
    stones_line_number = None

    for ln, text in lines:
        if text.startswith("===Stones:"):
            stones_line = text
            stones_line_number = ln
            break

    if stones_line is None:
        errors.append(f"[Section {section_number} @ line {start_line_number}] Missing ===Stones:")
        return

    # --- Parse integer part and optional -V ---
    m = re.match(r"^===Stones:\s*(\d+)(?:-V)?$", stones_line)
    if not m:
        errors.append(f"[Section {section_number} @ line {stones_line_number}] Invalid Stones line: {stones_line}")
        return

    expected_numbered = int(m.group(1))
    has_vacant_flag = stones_line.endswith("-V")

    # --- Collect stone blocks ---
    stone_blocks = []
    numbered_stones = []

    for ln, text in lines:
        if text.startswith("===Stone:"):
            stone_blocks.append((ln, text))
            m2 = re.match(r"^===Stone:\s*(\d+)$", text)
            if m2:
                numbered_stones.append((ln, int(m2.group(1))))
            elif text.strip() == "===Stone: VACANT":
                pass
            else:
                errors.append(f"[Section {section_number} @ line {ln}] Invalid Stone line: {text}")

    # --- Validate count of numbered stones ---
    actual_numbered = len(numbered_stones)

    if actual_numbered != expected_numbered:
        errors.append(
            f"[Section {section_number} @ line {stones_line_number}] Numbered stone count mismatch: expected {expected_numbered}, found {actual_numbered}"
        )

    # --- Special rule for 0-V ---
    if expected_numbered == 0 and has_vacant_flag:
        vacants = [1 for ln, text in stone_blocks if text.strip() == "===Stone: VACANT"]
        if len(vacants) != 1:
            errors.append(
                f"[Section {section_number} @ line {stones_line_number}] 0-V section must contain exactly one VACANT stone block"
            )
        if actual_numbered != 0:
            errors.append(
                f"[Section {section_number} @ line {stones_line_number}] 0-V section cannot contain numbered stones"
            )
        return

    # --- Validate descending order ---
    # Positions = number of stone blocks (numbered + VACANT)
    expected_position = len(stone_blocks)
    remaining_numbered = expected_numbered

    for ln, text in stone_blocks:

        # VACANT stone
        if text.strip() == "===Stone: VACANT":
            expected_position -= 1
            continue

        # Numbered stone
        m3 = re.match(r"^===Stone:\s*(\d+)$", text)
        if m3:
            num = int(m3.group(1))

            if num != expected_position:
                errors.append(
                    f"[Section {section_number} @ line {ln}] Stone number out of order: expected {expected_position}, found {num}"
                )

            expected_position -= 1
            remaining_numbered -= 1
            continue

        errors.append(
            f"[Section {section_number} @ line {ln}] Invalid Stone line: {text}"
        )

    # --- Final checks ---
    if remaining_numbered != 0:
        errors.append(
            f"[Section {section_number} @ line {start_line_number}] Numbered stones incomplete: expected to consume {expected_numbered}, remaining {remaining_numbered}"
        )

    if expected_position != 0:
        errors.append(
            f"[Section {section_number} @ line {start_line_number}] Stone positions incomplete: expected to reach 0, ended at {expected_position}"
        )


def validate_file(path):
    errors = []

    with open(path, "r", encoding="utf-8") as f:
        lines = [(i+1, line.rstrip("\n")) for i, line in enumerate(f)]

    # --- Split sections using EXACT delimiter ---
    sections = []
    current = []

    for ln, text in lines:

        # --- Detect corrupted delimiters explicitly ---
        if text.startswith("=") and "DIV80==" in text and text != SECTION_DELIMITER:
            errors.append(f"[Line {ln}] Corrupted delimiter: {text}")

        # --- Valid delimiter ---
        if text == SECTION_DELIMITER:
            if current:
                sections.append(current)
            current = []
            continue  # do NOT include delimiter in any section

        current.append((ln, text))

    if current:
        sections.append(current)

    # --- Validate each section ---
    for idx, sec in enumerate(sections, start=1):

        # NEW FEATURE: ignore section if PID says so
        first_line_text = sec[0][1]
        if first_line_text.startswith("===PID: IGNORE_SECTION"):
            continue

        start_ln = sec[0][0]
        validate_section(sec, idx, start_ln, errors)

    # --- Output ---
    if errors:
        print("Validation errors:")
        for e in errors:
            print(e)
    else:
        print("No validation errors found.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validator.py <cemetery_file.txt>")
        sys.exit(1)

    validate_file(sys.argv[1])
