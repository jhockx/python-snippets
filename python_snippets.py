def list_diff(list1, list2) -> list:
    """
    Get the difference between two lists
    
    :arg list1: First list for the difference
    :arg list2: Second list for the difference
    """
    return list(list(set(list1)-set(list2)) + list(set(list2)-set(list1)))
