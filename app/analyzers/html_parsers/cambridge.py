from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1017
def parse_cambridge(soup):

    is_french = False

    affiliations = {}
    authors = []
    for elt in soup.find_all(class_='aff'):
        nb_sup=0
        try:
            nb_sup = elt.find(class_='sup').get_text()
        except:
            try:
                nb_sup = elt.find(class_='label').get_text()
            except:
                nb_sup = 0

        structure_name = elt.get_text().strip()
        affiliations[nb_sup] = structure_name
        if re.search(fr_regex, structure_name.lower()):
            is_french = True

    authors    = []
    author_elt = soup.find(class_='author')
    if author_elt is not None:
        for elt in author_elt.children:
            if isinstance(elt, bs4.element.Tag) and elt.name=='a':
                full_name = elt.get_text().strip()
                author = {}
                author['full_name'] = full_name
                author['affiliations_info'] = []
                authors.append(author)
            if isinstance(elt, bs4.element.Tag) and "data-affiliation-id" in elt.attrs:
                aff_id = keep_digits(elt.get_text())
                if aff_id in affiliations:
                    author['affiliations_info'].append({'structure_name': affiliations[aff_id]})
                if len(affiliations)==1 and 0 in affiliations:
                    author['affiliations_info'].append({'structure_name':affiliations[0]})

    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
