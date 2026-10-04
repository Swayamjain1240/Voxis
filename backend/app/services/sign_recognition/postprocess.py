def suppress_duplicates(
    glosses: list[str],
    confidence: list[float],
    min_confidence: float = 0.60,
):
    """
    Removes repeated predictions and low-confidence results.

    This becomes part of Swayam's real-time post-processing
    after the trained model is available.
    """

    output_glosses = []
    output_confidence = []

    for gloss, score in zip(
        glosses,
        confidence,
    ):
        if (
            not gloss
            or score < min_confidence
        ):
            continue

        gloss = gloss.upper()

        if (
            output_glosses
            and output_glosses[-1] == gloss
        ):
            output_confidence[-1] = max(
                output_confidence[-1],
                score,
            )
            continue

        output_glosses.append(gloss)
        output_confidence.append(score)

    return (
        output_glosses,
        output_confidence,
    )


def reject_unknown(
    gloss: str,
    confidence: float,
    threshold: float = 0.60,
):
    if confidence < threshold:
        return {
            "gloss": "UNKNOWN",
            "confidence": confidence,
        }

    return {
        "gloss": gloss.upper(),
        "confidence": confidence,
    }
