from pathlib import Path

from apng import APNG


# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).parent.parent

FRAMES_DIR = ROOT / "frames"
TIMING_FILE = FRAMES_DIR / "timing.txt"

ASSETS_DIR = ROOT / "assets"
OUTPUT = ASSETS_DIR / "terminal.apng"


# ==========================================================
# Read Timing Metadata
# ==========================================================

def read_timing():

    timings = {}

    if not TIMING_FILE.exists():

        raise FileNotFoundError(
            f"Timing file not found: {TIMING_FILE}\n"
            "Run generate_frames.py first."
        )

    lines = TIMING_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    for line in lines:

        if not line.strip():
            continue

        parts = line.split()

        if len(parts) != 2:
            continue

        filename = parts[0]
        delay = int(parts[1])

        timings[filename] = delay

    return timings


# ==========================================================
# Build APNG
# ==========================================================

def main():

    # ------------------------------------------------------
    # Make sure assets directory exists
    # ------------------------------------------------------

    ASSETS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------
    # Read timing information
    # ------------------------------------------------------

    timings = read_timing()

    # ------------------------------------------------------
    # Find PNG frames
    # ------------------------------------------------------

    frames = sorted(
        FRAMES_DIR.glob(
            "frame*.png"
        )
    )

    if not frames:

        print("No PNG frames found.")
        print(
            "Run generate_frames.py first."
        )

        return

    # ------------------------------------------------------
    # Create APNG
    # ------------------------------------------------------

    animation = APNG()

    for frame in frames:

        filename = frame.name

        if filename not in timings:

            raise ValueError(
                f"No timing information found "
                f"for {filename}"
            )

        delay = timings[filename]

        animation.append_file(
            str(frame),
            delay=delay,
        )

        print(
            f"Added {filename} "
            f"({delay} ms)"
        )

    # ------------------------------------------------------
    # Save APNG
    # ------------------------------------------------------

    animation.save(
        str(OUTPUT)
    )

    # ------------------------------------------------------
    # Finished
    # ------------------------------------------------------

    print()
    print(
        "========================================"
    )
    print(
        "APNG generated successfully!"
    )
    print(
        f"Frames : {len(frames)}"
    )
    print(
        f"Output : {OUTPUT}"
    )
    print(
        "========================================"
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()