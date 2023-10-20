def str_to_bool(args):
    true_list = ["true", 1, "1", "yes"]
    false_list = ["false", 0, "0", "no"]

    if str(args).lower() in true_list:
        return True

    elif str(args).lower() in false_list:
        return False

    else:
        return None
