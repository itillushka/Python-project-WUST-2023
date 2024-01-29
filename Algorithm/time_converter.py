
def convert_ms_to_min_sec(ms):
    """
        Converts milliseconds to minutes and seconds.
    Args:
        ms (int): The time in milliseconds.
    Returns:
        str: The time in minutes and seconds, formatted as 'minutes:seconds'.
    """
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"