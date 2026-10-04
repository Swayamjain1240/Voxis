def validate_mode_1_access():
    """
    Mode 1 is intentionally a no-login hackathon MVP.

    This function provides one stable access boundary so authentication
    can be added later without rewriting route logic.
    """
    return True
