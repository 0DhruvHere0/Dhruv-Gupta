from pathlib import Path
from apng import APNG
ROOT = Path(__file__).parent.parent
FRAMES_DIR = ROOT / "frames"
TIMING_FILE = FRAMES_DIR / "timing.txt"
ASSETS_DIR = ROOT / "assets"
OUTPUT = ASSETS_DIR / "terminal.apng"
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
def main():
    ASSETS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    timings = read_timing()
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
    animation.save(
        str(OUTPUT)
    )
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
if __name__ == "__main__":
    main()