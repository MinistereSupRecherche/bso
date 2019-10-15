from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.3389
def parse_frontiers(soup):

    is_french = False

    authors, affiliations = [], {}
    for a_elt in soup.find_all(class_='notes'):
        for elt in a_elt.find_all('li'):
            is_elt_ok = False
            for sub_elt in elt.children:

                if(isinstance(sub_elt, bs4.element.Tag)) :

                    if sub_elt.find('sup') is not None:
                        nb_sup = sub_elt.find('sup').get_text()
                        is_elt_ok = True

                elif is_elt_ok:
                    affiliations[nb_sup] = sub_elt.strip()
                    if re.search(fr_regex, sub_elt.lower()):
                        is_french = True

    abs_elt =  soup.find(class_='JournalAbstract')
    if abs_elt is None:
        return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

    auth_elt = abs_elt.find(class_='authors')
    if auth_elt is None:
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

    for sub_elt in auth_elt.children:
        author = None
        if isinstance(sub_elt, bs4.element.Tag) and 'class' in sub_elt.attrs:
            full_name = sub_elt.get_text()

            author = {}
            author['full_name'] = full_name
            author['affiliations_info'] = []
            authors.append(author)

        elif isinstance(sub_elt, bs4.element.Tag) and 'sup' == sub_elt.name and author:
            nb_sups = sub_elt.get_text()
            for nb_sup in nb_sups.split(','):
                if nb_sup in affiliations:
                    author['affiliations_info'].append({'structure_name': affiliations[nb_sup]})



    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
