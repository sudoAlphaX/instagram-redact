from helpers.configutils import importconfig


def str_to_bool(args):
    true_list = ["true", 1, "1", "yes"]
    false_list = ["false", 0, "0", "no"]

    if args.lower() in true_list:
        return True

    elif args.lower() in false_list:
        return False

    else:
        return None


def get_config(section, key, default):
    return default if ((q := importconfig((section))) == None) else (q.get(key))
