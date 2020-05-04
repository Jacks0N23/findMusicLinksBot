def list_to_dict(lst):
    op = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return op
