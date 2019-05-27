
def contains_any_element(A, B):
    """
        Checks if at least one element from A exists in B
    """
    return not set(A).isdisjoint(B)