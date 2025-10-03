# scenes.py
# Defines both the navigation map and scene descriptions/images
# for Seal of Solara

SCENE_MAP = {
    # Forest hub
    ("forest", "north"): "mountain",
    ("mountain", "south"): "forest",

    ("forest", "east"): "lake",
    ("lake", "west"): "forest",

    ("lake", "south"): "cave",
    ("cave", "north"): "lake",

    ("forest", "west"): "ruins",
    ("ruins", "east"): "forest",

    ("forest", "south"): "swamp",
    ("swamp", "north"): "forest",

    # Mountain path to city
    ("mountain", "north"): "city",
    ("city", "south"): "mountain",
}

SCENES = {
    "forest": {
        "description": "Tall trees sway. A key glints nearby.",
        "description_key": "Tall trees sway.",
        "image": "/static/assets/forest_with_key.png"
    },
    "lake": {
        "description": "A fisherman hums by the shimmering lake.",
        "image": "/static/assets/lake.png"
    },
    "ruins": {
        "description": "Whispers echo through ancient stone.",
        "image": "/static/assets/ruins.png"
    },
    "swamp": {
        "description": "Mud clings to your feet. A twisted root glows faintly.",
        "image": "/static/assets/swamp.png"
    },
    "mountain": {
        "description": "Snow swirls. Boots lie half-buried in the ice.",
        "image": "/static/assets/mountain_with_boots.png"
    },
    "cave": {
        "description": "A glowing altar pulses with ancient energy.",
        "description_scroll": "The altar hums with power. Symbols swirl in the air.",
        "image": "/static/assets/cave_locked.png"
    },
    "city": {
        "description": "Golden gates shimmer. The seal awaits.",
        "description_seal": "Seal used. Light floods the streets. You win!",
        "image": "/static/assets/city_closed.png"
    }
}


