from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).parent.parent
ASCII_FILE = ROOT / "assets" / "ascii" / "profile.txt"
PROFILE_FILE = ROOT / "data" / "profile.txt"
SKILLS_FILE = ROOT / "data" / "skills.txt"
MYINFO_FILE = ROOT / "data" / "myinfo.txt"
SOCIALS_FILE = ROOT / "data" / "socials.txt"
FRAMES_DIR = ROOT / "frames"
TIMING_FILE = FRAMES_DIR / "timing.txt"
WIDTH = 1000
HEIGHT = 650
BACKGROUND = "#0d1117"
TITLEBAR = "#161b22"
TEXT = "#c9d1d9"
BLUE = "#58a6ff"
CYAN = "#79c0ff"
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
FONT_SIZE = 18
SMALL_FONT_SIZE = 14
ASCII_FONT_SIZE = 7
TYPING_DELAY = 60
OUTPUT_DELAY = 2500
EMPTY_DELAY = 600
def font(size):
    return ImageFont.truetype(
        FONT_PATH,
        size,
    )
def create_terminal():
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (0, 0, WIDTH, 48),
        fill=TITLEBAR,
    )
    draw.ellipse(
        (18, 17, 30, 29),
        fill="#ff5f56",
    )
    draw.ellipse(
        (38, 17, 50, 29),
        fill="#ffbd2e",
    )
    draw.ellipse(
        (58, 17, 70, 29),
        fill="#27c93f",
    )
    draw.text(
        (WIDTH // 2, 17),
        "Terminal",
        fill=TEXT,
        font=font(14),
        anchor="ma",
    )
    return image, draw
def draw_prompt(
    draw,
    command="",
    y=75,
    cursor=True,
):
    current_x = 30
    username = "dhruv@github"
    draw.text(
        (current_x, y),
        username,
        fill=BLUE,
        font=font(FONT_SIZE),
    )
    current_x += draw.textlength(
        username,
        font=font(FONT_SIZE),
    )
    path = " ~ %"
    draw.text(
        (current_x + 8, y),
        path,
        fill=TEXT,
        font=font(FONT_SIZE),
    )
    current_x += (
        draw.textlength(
            path,
            font=font(FONT_SIZE),
        )
        + 8
    )
    draw.text(
        (current_x, y),
        command,
        fill=CYAN,
        font=font(FONT_SIZE),
    )
    current_x += draw.textlength(
        command,
        font=font(FONT_SIZE),
    )
    if cursor:
        draw.rectangle(
            (
                current_x + 2,
                y + 2,
                current_x + 11,
                y + FONT_SIZE + 1,
            ),
            fill=TEXT,
        )
def read_file(path):
    return path.read_text(
        encoding="utf-8"
    ).splitlines()
def typing_sequence(command):
    return [
        command[:index]
        for index in range(
            1,
            len(command) + 1,
        )
    ]
def empty_screen():
    image, draw = create_terminal()
    draw_prompt(
        draw,
        "",
        75,
    )
    return image
def command_screen(
    command,
    y=75,
):
    image, draw = create_terminal()
    draw_prompt(
        draw,
        command,
        y,
    )
    return image
def neofetch_screen(
    next_command="",
):
    image, draw = create_terminal()
    draw_prompt(
        draw,
        "neofetch",
        75,
        cursor=False,
    )
    ascii_lines = read_file(
        ASCII_FILE
    )
    ascii_font = font(
        ASCII_FONT_SIZE
    )
    ascii_x = 25
    ascii_y = 125
    for line in ascii_lines:
        draw.text(
            (
                ascii_x,
                ascii_y,
            ),
            line,
            fill=BLUE,
            font=ascii_font,
        )
        ascii_y += 6
    profile_lines = read_file(
        PROFILE_FILE
    )
    info_x = 500
    info_y = 155
    for line in profile_lines:
        if "=" not in line:
            continue
        key, value = line.split(
            "=",
            1,
        )
        key_text = f"{key}:"
        draw.text(
            (
                info_x,
                info_y,
            ),
            key_text,
            fill=BLUE,
            font=font(SMALL_FONT_SIZE),
        )
        key_width = draw.textlength(
            key_text,
            font=font(SMALL_FONT_SIZE),
        )
        draw.text(
            (
                info_x + key_width + 10,
                info_y,
            ),
            value,
            fill=TEXT,
            font=font(SMALL_FONT_SIZE),
        )
        info_y += 28
    draw_prompt(
        draw,
        next_command,
        600,
    )
    return image
def build_skill_tree():
    lines = read_file(
        SKILLS_FILE
    )
    tree = []
    for line in lines:
        if not line.strip():
            continue
        indentation = (
            len(line)
            - len(line.lstrip())
        )
        name = line.strip()
        if indentation == 0:
            tree.append(
                (
                    0,
                    name,
                )
            )
        else:
            tree.append(
                (
                    1,
                    name,
                )
            )
    return tree
def skills_screen(
    next_command="",
):
    image, draw = create_terminal()
    draw_prompt(
        draw,
        "tree skills",
        75,
        cursor=False,
    )
    draw.text(
        (35, 125),
        "skills",
        fill=TEXT,
        font=font(FONT_SIZE),
    )
    tree = build_skill_tree()
    y = 160
    categories = [
        index
        for index, item in enumerate(tree)
        if item[0] == 0
    ]
    for index, (level, name) in enumerate(tree):
        if level == 0:
            category_position = categories.index(
                index
            )
            is_last_category = (
                category_position
                == len(categories) - 1
            )
            prefix = (
                "└── "
                if is_last_category
                else "├── "
            )
            draw.text(
                (35, y),
                prefix + name,
                fill=BLUE,
                font=font(SMALL_FONT_SIZE),
            )
        else:
            current_category = None
            for previous in range(
                index - 1,
                -1,
                -1,
            ):
                if tree[previous][0] == 0:
                    current_category = previous
                    break
            category_position = categories.index(
                current_category
            )
            next_category = (
                categories[
                    category_position + 1
                ]
                if category_position + 1
                < len(categories)
                else None
            )
            is_last_skill = (
                next_category is None
                or index == next_category - 1
            )
            prefix = (
                "    └── "
                if is_last_skill
                else "    ├── "
            )
            draw.text(
                (35, y),
                prefix + name,
                fill=TEXT,
                font=font(SMALL_FONT_SIZE),
            )
        y += 25
    draw_prompt(
        draw,
        next_command,
        min(
            y + 15,
            600,
        ),
    )
    return image
def text_file_screen(
    command,
    path,
    next_command="",
):
    image, draw = create_terminal()
    draw_prompt(
        draw,
        command,
        75,
        cursor=False,
    )
    lines = read_file(
        path
    )
    x = 35
    y = 125
    for line in lines:
        draw.text(
            (
                x,
                y,
            ),
            line,
            fill=TEXT,
            font=font(SMALL_FONT_SIZE),
        )
        y += 25
        if y > HEIGHT - 65:
            break
    prompt_y = min(
        y + 15,
        600,
    )
    draw_prompt(
        draw,
        next_command,
        prompt_y,
    )
    return image
def save_frame(
    image,
    number,
    delay,
    timing_entries,
):
    output = (
        FRAMES_DIR
        / f"frame{number:03d}.png"
    )
    image.save(
        output,
        "PNG",
    )
    timing_entries.append(
        (
            output.name,
            delay,
        )
    )
    print(
        f"Created {output.name} "
        f"({delay} ms)"
    )
def add_typing_frames(
    command,
    frame_number,
    timing_entries,
):
    for partial_command in typing_sequence(
        command
    ):
        save_frame(
            command_screen(
                partial_command
            ),
            frame_number,
            TYPING_DELAY,
            timing_entries,
        )
        frame_number += 1
    return frame_number
def add_neofetch_clear_frames(
    frame_number,
    timing_entries,
):
    for partial_command in typing_sequence(
        "clear"
    ):
        save_frame(
            neofetch_screen(
                partial_command
            ),
            frame_number,
            TYPING_DELAY,
            timing_entries,
        )
        frame_number += 1
    return frame_number
def add_skills_clear_frames(
    frame_number,
    timing_entries,
):
    for partial_command in typing_sequence(
        "clear"
    ):
        save_frame(
            skills_screen(
                partial_command
            ),
            frame_number,
            TYPING_DELAY,
            timing_entries,
        )
        frame_number += 1
    return frame_number
def add_text_clear_frames(
    command,
    path,
    frame_number,
    timing_entries,
):
    for partial_command in typing_sequence(
        "clear"
    ):
        save_frame(
            text_file_screen(
                command,
                path,
                partial_command,
            ),
            frame_number,
            TYPING_DELAY,
            timing_entries,
        )
        frame_number += 1
    return frame_number
def write_timing_file(
    timing_entries,
):
    with TIMING_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        for filename, delay in timing_entries:
            file.write(
                f"{filename} {delay}\n"
            )
def main():
    FRAMES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    for file in FRAMES_DIR.glob(
        "*.png"
    ):
        file.unlink()
    if TIMING_FILE.exists():
        TIMING_FILE.unlink()
    frame_number = 1
    timing_entries = []
    save_frame(
        empty_screen(),
        frame_number,
        EMPTY_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_typing_frames(
        "neofetch",
        frame_number,
        timing_entries,
    )
    save_frame(
        neofetch_screen(
            ""
        ),
        frame_number,
        OUTPUT_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_neofetch_clear_frames(
        frame_number,
        timing_entries,
    )
    save_frame(
        empty_screen(),
        frame_number,
        EMPTY_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_typing_frames(
        "tree skills",
        frame_number,
        timing_entries,
    )
    save_frame(
        skills_screen(
            ""
        ),
        frame_number,
        OUTPUT_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_skills_clear_frames(
        frame_number,
        timing_entries,
    )
    save_frame(
        empty_screen(),
        frame_number,
        EMPTY_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_typing_frames(
        "cat myinfo.txt",
        frame_number,
        timing_entries,
    )
    save_frame(
        text_file_screen(
            "cat myinfo.txt",
            MYINFO_FILE,
            "",
        ),
        frame_number,
        OUTPUT_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_text_clear_frames(
        "cat myinfo.txt",
        MYINFO_FILE,
        frame_number,
        timing_entries,
    )
    save_frame(
        empty_screen(),
        frame_number,
        EMPTY_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_typing_frames(
        "cat socials.txt",
        frame_number,
        timing_entries,
    )
    save_frame(
        text_file_screen(
            "cat socials.txt",
            SOCIALS_FILE,
            "",
        ),
        frame_number,
        OUTPUT_DELAY,
        timing_entries,
    )
    frame_number += 1
    frame_number = add_text_clear_frames(
        "cat socials.txt",
        SOCIALS_FILE,
        frame_number,
        timing_entries,
    )
    save_frame(
        empty_screen(),
        frame_number,
        EMPTY_DELAY,
        timing_entries,
    )
    write_timing_file(
        timing_entries
    )
    print()
    print(
        "========================================"
    )
    print(
        "PNG frames generated successfully!"
    )
    print(
        f"Frames : {len(timing_entries)}"
    )
    print(
        f"Timing : {TIMING_FILE}"
    )
    print(
        f"Output : {FRAMES_DIR}"
    )
    print(
        "========================================"
    )
if __name__ == "__main__":
    main()