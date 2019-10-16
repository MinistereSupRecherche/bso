"""Detection of country for authors affiliations."""
import requests
from bs4 import BeautifulSoup
# from typing import Union, List, Dict, Any


def get_references_from_hal(hal_id: str):
    url = "https://hal.archives-ouvertes.fr/{}/html_references".format(hal_id)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        references = []
        for doi_reference in soup.find_all(class_='doi-reference-value'):
            references.append('doi' + doi_reference.get_text().lower())
        references = list(set(references))
        return references
    except Exception:
        print("error in hal getting references for id hal {}".format(hal_id))
        return []
