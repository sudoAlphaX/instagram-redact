def str_to_bool(args):
    """
    The str_to_bool function takes a string as an argument and returns the corresponding boolean value, or None.

    Args:
        args: Pass in the arguments that are passed into the function

    Returns:
        A boolean value

    Doc Author:
        Trelent
    """

    true_list = ["true", 1, "1", "yes"]
    false_list = ["false", 0, "0", "no"]

    if str(args).lower() in true_list:
        return True

    elif str(args).lower() in false_list:
        return False

    else:
        return None
