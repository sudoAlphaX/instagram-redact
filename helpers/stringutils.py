def str_to_bool(args, fallback=False):
    """
    The str_to_bool function takes a string or boolean as an argument and returns the corresponding boolean value,
    or the original value if fallback is True and the string does not match any of the expected values.

    Args:
        args: Pass in the arguments that are passed into the function
        fallback: If True, the function will return args when it doesn't match any value in the lists. Defaults to False.

    Returns:
        A boolean value, original argument value or None

    Doc Author:
        Trelent
    """

    if isinstance(args, bool):
        return args

    true_list = ["true", "1", "yes", "y"]
    false_list = ["false", "0", "no", "n"]

    if str(args).lower() in true_list:
        return True

    elif str(args).lower() in false_list:
        return False

    elif fallback:
        return args

    else:
        return None
