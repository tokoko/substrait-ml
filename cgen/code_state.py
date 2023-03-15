global active_code
active_code = []


def get_active_code():
    global active_code
    return active_code[-1] if active_code else None