from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1039
def parse_rsc(soup):

    is_french = False

    authors, affiliations = [], {}

    is_ok = False
    for elt in soup.find_all(class_='article__author-affiliation'):

        if elt.find('sup'):
            nb_sup = elt.find('sup').get_text()
            is_ok = True

        if elt.find('span') and is_ok:
            structure_name = elt.find_all('span')[1].get_text().strip()
            is_ok = False
            affiliations[nb_sup] = structure_name
            if re.search(fr_regex, structure_name.lower()):
                is_french = True

    for author_elt in soup.find_all(class_='article__author-link'):
        if author_elt.find('a'):
            full_name = author_elt.find('a').get_text()
            author = {}
            author['full_name'] = full_name
            author['affiliations_info'] = []
            authors.append(author)
        if author_elt.find('sup'):
            sups = author_elt.find('sup')
            if sups:
                for sup in sups.get_text().split(','):
                    if sup in affiliations:
                        author['affiliations_info'].append({'structure_name': affiliations[sup]})

    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
