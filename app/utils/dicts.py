"""Dictionnaries utils."""
from typing import Dict


def delete_nulls(dct: Dict, only_none: bool = False) -> Dict:
    """Delete null keys in a dictionnary.

    Args
        only_none: If True, only None keys are deleted.
            Otherwise delete all None, False, 0. Default to False.
    Returns
        A dictionnary without empty values

    """
    if only_none is True:
        new_dct = {k: v for k, v in dct.items() if v is not None}
    else:
        new_dct = {k: v for k, v in dct.items() if v}

    for k, v in new_dct.items():
        if isinstance(v, dict):
            new_dct[k] = delete_nulls(v, only_none=True)
        if isinstance(v, list):
            for i, elem in enumerate(v):
                if isinstance(elem, dict):
                    v[i] = delete_nulls(elem, only_none=True)
            new_dct[k] = v
    if only_none is True:
        new_dct = {k: v for k, v in dct.items() if v is not None}
    else:
        new_dct = {k: v for k, v in dct.items() if v}
    return new_dct


def compare_dicts(source: Dict, snapshot: Dict) -> Dict:
    """
    Compare two dictionaries.

    Return only changed field.
    If the field is a list, it returns a list with all elements
    from source that are not in snapshot.
    """
    changes = {}
    for k, v in source.items():
        snap_value = snapshot.get(k, None)
        if v and not snap_value:
            changes[k] = v
        else:
            if isinstance(v, list):
                field = []
                for elem in v:
                    if elem not in snap_value:
                        field.append(elem)
                if field:
                    changes[k] = v
            else:
                if snap_value != v:
                    changes[k] = v
    return changes
