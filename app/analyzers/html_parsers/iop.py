from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1088
def parse_iop(soup):

    is_french = False

    authors, affiliations = [], {}

    for elt in soup.find_all(class_='mb-05'):
        is_elt_ok = False
        for sub_elt in elt.children:
            if(isinstance(sub_elt, bs4.element.Tag)) :
                if sub_elt.name=='sup':
                    nb_sup = sub_elt.get_text()
                    is_elt_ok = True
            elif is_elt_ok:
                affiliations[nb_sup] = sub_elt.strip()
                if re.search(fr_regex, sub_elt.lower()):
                    is_french = True


    for author_elt in soup.find_all('span', {'itemprop':'author'}):
        author = {}
        for sub_elt in author_elt:

            if isinstance(sub_elt, bs4.element.NavigableString):
                full_name = sub_elt

        if author_elt.find('sup') is None:
            continue
        nb_sups = author_elt.find('sup').get_text().split(',')
        full_name = author_elt.find('span').get_text()
        author['full_name'] = full_name
        author['affiliations_info'] = []
        for nb_sup in nb_sups:
            if nb_sup in affiliations:
                author['affiliations_info'].append({'structure_name': affiliations[nb_sup]})
        authors.append(author)


    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
