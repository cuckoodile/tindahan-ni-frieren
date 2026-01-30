def formatName(name: str) -> str:
    """Formats a name string to have the first letter of each word capitalized.

    Args:
        name (str): The name string to format.

    Returns:
        str: The formatted name string.
    """

    return ' '.join(name.title().split())

def formatMiddleName(middle_name: str) -> str:
    """Formats a middle name string to be a single uppercase initial followed by a period.
    If the middle name is empty or None, returns an empty string.

    Args:
        middle_name (str): The middle name string to format.
    """
    if middle_name and middle_name.strip():
        return f"{middle_name.strip()[0].upper()}."
    return ""