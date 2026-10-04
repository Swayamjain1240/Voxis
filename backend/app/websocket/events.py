import time


def build_event(
    event_type: str,
    data: dict | None = None,
):
    return {
        "type": event_type,
        "data": data or {},
        "timestamp": int(
            time.time() * 1000
        ),
    }


class EventTypes:
    SYSTEM_READY = "system.ready"

    SPEECH_STARTED = "speech.started"
    SPEECH_TRANSCRIPT = "speech.transcript"

    GLOSS_UPDATED = "gloss.updated"

    SIGN_PREDICTION = "sign.prediction"

    AVATAR_PLAY = "avatar.play"

    CONVERSATION_MESSAGE = (
        "conversation.message"
    )
