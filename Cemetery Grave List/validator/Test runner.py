import subprocess
import tempfile
import os

def run_validator(validator_path, text):
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write(text)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["python", validator_path, tmp_path],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    finally:
        os.remove(tmp_path)


TESTS = [

    # --------------------------------------------------------
    # DELIMITER TESTS
    # --------------------------------------------------------
    ("Valid delimiter",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Date:\n",
     True),

    ("Corrupted delimiter",
     "======================================================================DIV80==\n",
     False),

    ("Missing delimiter",
     "===PID: A\n",
     False),

    # --------------------------------------------------------
    # HEADER TESTS
    # --------------------------------------------------------
    ("Missing PID",
     "=========================================================================DIV80==\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Date:\n",
     False),

    ("Wrong header order",
     "=========================================================================DIV80==\n===PID: A\n===Place: Y\n===Coord: X\n===Stones: 0-V\n===Date:\n",
     False),

    ("IGNORE_SECTION",
     "=========================================================================DIV80==\n===PID: IGNORE_SECTION\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Date:\n",
     True),

    # --------------------------------------------------------
    # STONES HEADER TESTS
    # --------------------------------------------------------
    ("Valid Stones N",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 3\n"
     "===Stone: 3\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Stone: 2\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    ("Valid Stones N-V",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 3-V\n"
     "===Stone: 3\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Stone: 2\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    ("Valid Stones 0-V",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Date:\n",
     True),

    ("Invalid Stones 0",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0\n",
     False),

    ("Invalid Stones -V",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: -V\n",
     False),

    # --------------------------------------------------------
    # ZERO-STONE TESTS
    # --------------------------------------------------------
    ("0-V no dated-entry sets",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n",
     False),

    ("0-V with Date",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Date:\n",
     True),

    ("0-V with Photos",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Photos:\n",
     True),

    ("0-V with Notes",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Notes:\n",
     True),

    ("0-V with stone block present",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 0-V\n===Stone: 1\n",
     False),

    # --------------------------------------------------------
    # NUMBERED STONE TESTS
    # --------------------------------------------------------
    ("Correct number of stones",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n"
     "===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    ("Wrong number of stones",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 2\n===Stone: 1\n",
     False),

    ("Non-consecutive numbering",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 3\n===Stone: 3\n===Stone: 1\n",
     False),

    ("VACANT stone allowed",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n"
     "===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n"
     "===Date:\n===Photos:\n===Notes:\n"
     "===Stone: VACANT\n"
     "===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    # --------------------------------------------------------
    # TRANSCRIPTION BLOCK TESTS
    # --------------------------------------------------------
    ("Missing begin marker",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\n===Transcription:\ntext\n---------------------------------------------end-----DIV60--\n",
     False),

    ("Missing end marker",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n",
     False),

    ("Empty transcription",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\n---------------------------------------------end-----DIV60--\n",
     False),

    # --------------------------------------------------------
    # DATED-ENTRY SET TESTS
    # --------------------------------------------------------
    ("Valid dated-entry set",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n===Date:\n===Photos:\n===Notes:\n===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    ("Text between Photos and Notes allowed",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\n===Transcription:\n---------------------------------------------begin---DIV60--\ntext\n---------------------------------------------end-----DIV60--\n===Date:\n===Photos:\ntext A\ntext B\n===Notes:\n===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     True),

    ("No lines allowed between Date and Photos",
     "=========================================================================DIV80==\n===PID: A\n===Coord: X\n===Place: Y\n===Stones: 1\n===Stone: 1\n===Date:\ntext\n===Photos:\n===Notes:\n===Interpretation:\n===Location:\n===Table:\n===Status:\n",
     False),
]


def run_all_tests(validator_path):
    print("Running test suite...\n")
    passed = 0

    for name, sample, expected_pass in TESTS:
        output = run_validator(validator_path, sample)
        ok = ("No validation errors found" in output)
        result = (ok == expected_pass)
        status = "PASS" if result else "FAIL"

        print(f"{status}: {name}")

        if not result:
            print("  Validator output:")
            print("  " + output.replace("\n", "\n  "))
            print()

        if result:
            passed += 1

    print(f"\n{passed} / {len(TESTS)} tests passed.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python test_runner.py <validator_script.py>")
        sys.exit(1)

    run_all_tests(sys.argv[1])
