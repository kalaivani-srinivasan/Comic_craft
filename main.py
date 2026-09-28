from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from PIL import Image, ImageDraw, ImageFont

import os
import textwrap


app = FastAPI(title="ComicCraft - AI Comic Story Creator")


# =========================================================
# FOLDERS
# =========================================================

STATIC_FOLDER = "static"
IMAGE_FOLDER = os.path.join(STATIC_FOLDER, "images")
TEMPLATE_FOLDER = "templates"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_FOLDER),
    name="static"
)

templates = Jinja2Templates(
    directory=TEMPLATE_FOLDER
)


# =========================================================
# FONT
# =========================================================

def get_font(size, bold=False):

    if bold:
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf"
        ]
    else:
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf"
        ]

    for font_path in font_paths:

        if os.path.exists(font_path):

            try:
                return ImageFont.truetype(
                    font_path,
                    size
                )
            except Exception:
                pass

    return ImageFont.load_default()


# =========================================================
# DELETE OLD PANELS
# =========================================================

def delete_old_images():

    for index in range(1, 6):

        file_path = os.path.join(
            IMAGE_FOLDER,
            f"panel_{index}.png"
        )

        if os.path.exists(file_path):
            os.remove(file_path)


# =========================================================
# CREATE STORY
# =========================================================

def create_story(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):

    story = f"""
COMICCRAFT - {character_name}'S ADVENTURE

STORY IDEA:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}


PANEL 1 - THE BEGINNING

{character_name} begins an exciting adventure
in the {setting}.

"{character_name}: Something tells me this
adventure is only beginning..."


PANEL 2 - THE DISCOVERY

While exploring the {setting},
{character_name} discovers something unexpected.

"{character_name}: What is this?
There must be something important here."


PANEL 3 - THE DANGER

A dangerous obstacle appears in the {setting}.
{character_name} must face the danger.

"{character_name}: I won't run away.
I'll face this!"


PANEL 4 - THE BATTLE

{character_name} uses courage and intelligence
to overcome the danger.

"{character_name}: I have to keep going!"


PANEL 5 - THE ENDING

The conflict is resolved.
The {setting} becomes peaceful again.

"{character_name}: We did it...
but this isn't the end."


END OF COMIC
"""

    return story


# =========================================================
# CREATE ONE COMIC PANEL
# =========================================================

def create_single_panel(
    index,
    title,
    character_name,
    setting,
    tone,
    art_style,
    scene_description
):

    width = 1200
    height = 800

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # OUTER BORDER
    # -----------------------------------------------------

    draw.rectangle(
        [10, 10, width - 10, height - 10],
        outline="black",
        width=8
    )

    # -----------------------------------------------------
    # TITLE BOX
    # -----------------------------------------------------

    title_font = get_font(
        42,
        bold=True
    )

    draw.rectangle(
        [30, 30, width - 30, 130],
        outline="black",
        width=4
    )

    draw.text(
        (60, 55),
        f"PANEL {index} - {title}",
        fill="black",
        font=title_font
    )

    # -----------------------------------------------------
    # MAIN SCENE
    # -----------------------------------------------------

    draw.rectangle(
        [50, 160, width - 50, 570],
        outline="black",
        width=5
    )

    # -----------------------------------------------------
    # GROUND
    # -----------------------------------------------------

    draw.line(
        [(70, 500), (1130, 500)],
        fill="black",
        width=6
    )

    # -----------------------------------------------------
    # SUN
    # -----------------------------------------------------

    draw.ellipse(
        [900, 200, 1030, 330],
        outline="black",
        width=6
    )

    # -----------------------------------------------------
    # CHARACTER
    # -----------------------------------------------------

    character_x = 400
    character_y = 300

    # Head

    draw.ellipse(
        [
            character_x - 60,
            character_y - 60,
            character_x + 60,
            character_y + 60
        ],
        outline="black",
        width=7
    )

    # Body

    draw.line(
        [
            (character_x, character_y + 60),
            (character_x, character_y + 230)
        ],
        fill="black",
        width=8
    )

    # Left arm

    draw.line(
        [
            (character_x, character_y + 100),
            (character_x - 100, character_y + 160)
        ],
        fill="black",
        width=8
    )

    # Right arm

    draw.line(
        [
            (character_x, character_y + 100),
            (character_x + 100, character_y + 160)
        ],
        fill="black",
        width=8
    )

    # Left leg

    draw.line(
        [
            (character_x, character_y + 230),
            (character_x - 80, character_y + 340)
        ],
        fill="black",
        width=8
    )

    # Right leg

    draw.line(
        [
            (character_x, character_y + 230),
            (character_x + 80, character_y + 340)
        ],
        fill="black",
        width=8
    )

    # -----------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------

    small_font = get_font(
        28,
        bold=True
    )

    draw.text(
        (650, 350),
        f"Setting: {setting}",
        fill="black",
        font=small_font
    )

    draw.text(
        (650, 400),
        f"Style: {art_style}",
        fill="black",
        font=small_font
    )

    draw.text(
        (650, 450),
        f"Tone: {tone}",
        fill="black",
        font=small_font
    )

    # -----------------------------------------------------
    # DESCRIPTION BOX
    # -----------------------------------------------------

    draw.rectangle(
        [50, 600, width - 50, 750],
        outline="black",
        width=4
    )

    description_font = get_font(24)

    wrapped_text = textwrap.fill(
        scene_description,
        width=80
    )

    draw.multiline_text(
        (75, 625),
        wrapped_text,
        fill="black",
        font=description_font,
        spacing=8
    )

    # -----------------------------------------------------
    # HERO NAME
    # -----------------------------------------------------

    draw.text(
        (700, 700),
        f"Hero: {character_name}",
        fill="black",
        font=small_font
    )

    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    file_path = os.path.join(
        IMAGE_FOLDER,
        f"panel_{index}.png"
    )

    image.save(file_path)

    return f"/static/images/panel_{index}.png"


# =========================================================
# CREATE ALL PANELS
# =========================================================

def create_panel_images(
    character_name,
    setting,
    tone,
    art_style
):

    delete_old_images()

    panels = [
        (
            "THE BEGINNING",
            f"{character_name} enters the {setting} "
            f"and begins an exciting adventure."
        ),
        (
            "THE DISCOVERY",
            f"{character_name} discovers a mysterious "
            f"secret inside the {setting}."
        ),
        (
            "THE DANGER",
            f"A dangerous creature appears in the {setting}. "
            f"{character_name} bravely faces the danger."
        ),
        (
            "THE BATTLE",
            f"{character_name} fights the danger "
            f"and protects the {setting}."
        ),
        (
            "THE ENDING",
            f"The danger is defeated. "
            f"{character_name} stands peacefully "
            f"inside the beautiful {setting}."
        )
    ]

    image_paths = []

    for index, panel in enumerate(
        panels,
        start=1
    ):

        title = panel[0]
        description = panel[1]

        path = create_single_panel(
            index=index,
            title=title,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            scene_description=description
        )

        image_paths.append(path)

        print(
            f"Panel {index} created successfully"
        )

    return image_paths


# =========================================================
# HOME
# =========================================================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================================================
# GENERATE COMIC
# =========================================================

@app.post("/generate")
async def generate(request: Request):

    form_data = await request.form()

    story_prompt = str(
        form_data.get(
            "story_prompt",
            "A mysterious adventure"
        )
    ).strip()

    character_name = str(
        form_data.get(
            "character_name",
            "Hero"
        )
    ).strip()

    setting = str(
        form_data.get(
            "setting",
            "Enchanted Forest"
        )
    ).strip()

    tone = str(
        form_data.get(
            "tone",
            "Adventure"
        )
    ).strip()

    art_style = str(
        form_data.get(
            "art_style",
            "Comic Book"
        )
    ).strip()

    # -----------------------------------------------------
    # CREATE STORY
    # -----------------------------------------------------

    story = create_story(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    # -----------------------------------------------------
    # CREATE PANELS
    # -----------------------------------------------------

    try:

        image_paths = create_panel_images(
            character_name,
            setting,
            tone,
            art_style
        )

    except Exception as error:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": (
                    f"Comic Generation Error: "
                    f"{type(error).__name__}: {error}"
                ),
                "story_prompt": story_prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "art_style": art_style
            }
        )

    # -----------------------------------------------------
    # SHOW RESULT
    # -----------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "story": story,
            "image_paths": image_paths,
            "story_prompt": story_prompt,
            "character_name": character_name,
            "setting": setting,
            "tone": tone,
            "art_style": art_style
        }
    )