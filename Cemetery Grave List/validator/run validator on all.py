import subprocess
import sys
from pathlib import Path


GRAVE_ROOT = Path(
    r"C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave"
)
SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "cemetery_file_validator.py"
OUTPUT_DIR = SCRIPT_DIR / "HIDE_validation-output"

VALIDATIONS = (
    (
        Path("DE, Bayern, Main-Spessart")
        / "Waldzell"
        / "Friedhof Waldzell - Grave List.txt",
        "out-Waldzell.txt",
    ),
    (
        Path("DE, Bayern, Schweinfurt")
        / "Oberschwarzach"
        / "Friedhof Oberschwarzach - Grave List.txt",
        "out-Oberschwarzach.txt",
    ),
    (
        Path("DE, Bayern, Main-Spessart")
        / "Hausen"
        / "Friedhof Hausen - Grave List.txt",
        "out-Hausen.txt",
    ),
    (
        Path("DE, Bayern, Main-Spessart")
        / "Unknown"
        / "Friedhof Unknown - Grave List.txt",
        "out-unknown.txt",
    ),
    (
        Path("DE, Bayern, Main-Spessart")
        / "Urspringen"
        / "Friedhof Urspringen - Grave List.txt",
        "out-Urspringen.txt",
    ),
    (
        Path("USA")
        / "Kealakekua - Kona Hongwanji Mission Cemetery"
        / "Kona Hongwanji Mission Cemetery - Grave List.txt",
        "out-Kona.txt",
    ),
)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    for relative_input, output_name in VALIDATIONS:
        print(" ===================================")
        input_path = GRAVE_ROOT / relative_input
        output_path = OUTPUT_DIR / output_name
        with output_path.open("wb") as output_file:
            subprocess.run(
                [sys.executable, str(VALIDATOR), str(input_path)],
                stdout=output_file,
                check=False,
            )

    print(" ===================================")


if __name__ == "__main__":
    main()
