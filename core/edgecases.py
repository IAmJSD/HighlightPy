all_to_int = lambda x: [int(y.strip()) for y in x]
# Converts everything in a list to a integer.


def int_list_or_none(possible_list):
    """Checks if something can be a integer list. If it can't, returns None."""
    if not possible_list:
        return

    try:
        return all_to_int(possible_list.split(","))
    except ValueError:
        pass
