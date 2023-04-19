def validate_name(name):
    if len(name) > 50 or 2 > len(name):
        return False
    return True