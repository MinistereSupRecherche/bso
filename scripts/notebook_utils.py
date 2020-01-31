import string
import unicodedata
import collections
import re
from typing import Dict


def strip_accents(w: str) -> str:
    """Normalize accents and stuff in string."""
    w2 = w.replace("’", " ")
    return "".join(
        c for c in unicodedata.normalize("NFD", w2)
        if unicodedata.category(c) != "Mn")


def delete_punct(w: str) -> str:
    """Delete all puctuation in a string."""
    return w.lower().translate(
        str.maketrans(string.punctuation, len(string.punctuation)*" "))


def generate_str_id_from_dict(dct: Dict, sort: bool = True) -> str:
    """Return a normalized stringify dict."""
    return normalize_text(stringify_dict(dct, sort=sort))


def stringify_dict(dct: Dict, sort: bool = True) -> str:
    """Stringify a dictionnary."""
    text = ""
    if sort is True:
        for k, v in collections.OrderedDict(dct).items():
            text += str(v)
    else:
        for k, v in dct.items():
            text += str(v)
    return text


def normalize_text(text: str) -> str:
    """Normalize string. Delete puctuation and accents."""
    if isinstance(text, str):
        text = delete_punct(text)
        text = strip_accents(text)
        text = text.replace('\xa0', ' ')
        text = " ".join(text.split())
    return text or ""


def normalize_name(text):
    return normalize_text(text).upper().replace('-', ' ')\
            .replace('‐', ' ').replace('  ', ' ')


def normalize_doi(doi):
    # remove / at the end of the doi and lower it
    doi_normalized = re.sub("(/){1,}$", "", doi.lower())
    doi_normalized = doi_normalized.replace("%2f", "/")
    return doi_normalized


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def clean_object(obj):
    for field in ['modified_at', 'created_at', '_id', 'etag', 'hrefs']:
        if field in obj:
            del obj[field]

    for e in obj:
        if isinstance(obj[e], list) \
                and len(obj[e]) > 0 \
                and isinstance(obj[e][0], dict) \
                and 'meta' in obj[e][0]:
            for elt in obj[e]:
                del elt['meta']
    return obj


def enrich_authors_info(persons, publi):
    doi = publi['doi']
    for p in persons:
        p['data_source'] = 'http://doi.org/'+doi
        if 'affiliations_info' in p and p['affiliations_info']:
            for k in p['affiliations_info']:
                k['start_date'] = publi['publication_date']
        if 'affiliations_info' in p and (not p['affiliations_info']):
            del p['affiliations_info']
