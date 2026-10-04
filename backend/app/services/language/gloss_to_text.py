TEMPLATES = {
    ("DOCTOR",): "Doctor.",
    ("PATIENT",): "The patient.",
    ("MEDICINE",): "Medicine.",
    ("HELP",): "I need help.",
    ("PAIN",): "I have pain.",
    ("YES",): "Yes.",
    ("NO",): "No.",
    ("WHERE", "PAIN"):
        "Where is the pain?",
    ("PAIN", "DOCTOR"):
        "I have pain. I need a doctor.",
    ("MEDICINE", "SICK"):
        "I am sick and need medicine.",
}


def gloss_to_text(
    glosses: list[str],
) -> str:
    normalized = tuple(
        item.strip().upper()
        for item in glosses
        if item and item.strip()
    )

    if not normalized:
        return ""

    if normalized in TEMPLATES:
        return TEMPLATES[
            normalized
        ]

    return " ".join(
        item.capitalize()
        for item in normalized
    )
