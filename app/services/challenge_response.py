def check_head_challenge(direction, session):

    if session.challenge == "LEFT":
        return direction == "left"

    if session.challenge == "RIGHT":
        return direction == "right"

    return True
