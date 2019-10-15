from typing import List, Dict, Any
import re
from app.utils.logger import create_logger


logger = create_logger(__name__)


def normalize_doi(doi):
    # remove / at the end of the doi and lower it
    doi_normalized = re.sub("(/){1,}$", "", doi.lower())
    doi_normalized = doi_normalized.replace("%2f", "/")
    return doi_normalized


def add_elt(old_elt_list: List, new_elt) -> List:
    new_elt_list = old_elt_list
    new_elt_list.append(new_elt)
    return list(set(new_elt_list))


def add_object(old_object_list: List, new_object: Dict) -> List:

    # if there is just an extra field 'id' => add it
    for elt in old_object_list:
        shared_items = {
            k: elt[k] for k in elt
            if k in new_object and elt[k] == new_object[k]
        }
        if 'id' in shared_items or \
                ('last_name' in shared_items and 'first_name' in shared_items):
            for field in new_object:
                elt[field] = new_object[field]

    # add extra element in the list for the other cases
    res = []

    for elt in old_object_list + [new_object]:
        if elt not in res:
            res.append(elt)

    return res


def update_elt(old_elt: Any, new_elt: Any) -> Any:

        if new_elt is None:
            return old_elt
        if isinstance(old_elt, str) and isinstance(new_elt, str):
            logger.debug("update str str")
            return new_elt
        if isinstance(old_elt, bool) and isinstance(new_elt, bool):
            logger.debug("update bool bool")
            return new_elt
        if isinstance(old_elt, float) and isinstance(new_elt, float):
            logger.debug("update float float")
            return new_elt
        elif isinstance(old_elt, list) and isinstance(new_elt, str):
            logger.debug("update list str")
            return add_elt(old_elt, new_elt)
        elif isinstance(old_elt, list) and isinstance(new_elt, dict):
            logger.debug("update list dict")
            return add_object(old_elt, new_elt)
        elif isinstance(old_elt, dict) and isinstance(new_elt, dict):
            for k in new_elt:
                logger.debug("updating dict field {}".format(k))
                if new_elt[k] is None:
                    continue
                elif k not in old_elt:
                    old_elt[k] = new_elt[k]
                else:
                    old_elt[k] = update_elt(old_elt[k], new_elt[k])
            return old_elt
        elif isinstance(old_elt, list) and isinstance(new_elt, list):
            logger.debug("update list list")
            logger.debug("old_elt = {}".format(old_elt))
            logger.debug("new_elt = {}".format(new_elt))
            
            for k in new_elt:
                if isinstance(k, dict):
                    old_elt = add_object(old_elt, k)
                else:
                    if k not in old_elt:
                        old_elt.append(k)
            return old_elt
        else:
            print("update not implemented for \
                {} - {}".format(type(old_elt), type(new_elt)))
            print("old: {} --- new: {}".format(old_elt, new_elt))
            print()
            print()
            print()
            print()
            return


def unique_id_external(id_external: List) -> List:
    ans: List = []
    for e in id_external:
        if e not in ans:
            ans.append(e)
    return ans
