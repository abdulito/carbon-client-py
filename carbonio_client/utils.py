__author__ = 'abdul'

########################################################################################################################
# Helpers
########################################################################################################################

def dict_deep_merge(source, destination):
    """
    deep merge of two dicts
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            dict_deep_merge(value, node)
        else:
            destination[key] = value

    return destination
