from collections import OrderedDict


def list_diff(list1, list2) -> list:
    """
    Get the difference between two lists
    
    :arg list1: First list for the difference
    :arg list2: Second list for the difference
    """
    return list(list(set(list1) - set(list2)) + list(set(list2) - set(list1)))


def list_drop_duplicates(li: list, keep: str = 'first') -> list:
    """
    Drop duplicates from a (ordered) list

    :param li: List to drop duplicates from
    :param keep: Keep first or last occurrence of the unique items
    """
    if keep == 'first':
        return list(OrderedDict((x, True) for x in li).keys())
    elif keep == 'last':
        li.reverse()
        li = list(OrderedDict((x, True) for x in li).keys())
        li.reverse()
        return li
    else:
        raise ValueError(f'Cannot parse {keep} as argument for keep. This should be either "first" or "last"')
