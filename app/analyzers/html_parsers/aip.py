from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1063
def parse_aip(soup):
    is_french = False

    authors, affiliations =[], {}
    for elt in soup.find_all(class_='author-affiliation'):
        try:
            nb_sup  =elt.find('sup').get_text()
        except:
            nb_sup = 0
        structure_name = elt.get_text().strip()
        affiliations[nb_sup] = structure_name

        if re.search(fr_regex, structure_name.lower()):
            is_french = True

    for elt in soup.find_all(class_='contrib-author'):
        author={}
        try:
            full_name = elt.find_all('a')[-1].get_text().strip()
            author['full_name'] = full_name
            author['affiliations_info'] = []
            authors.append(author)
        except:
            continue
        for sub_elt in elt.find_all('sup'):
            try:
                nb_sup = sub_elt.get_text()
                if nb_sup in affiliations:
                    author['affiliations_info'].append({'structure_name':affiliations[nb_sup]})
                elif len(affiliations)==1:
                    author['affiliations_info'].append({'structure_name':affiliations[0]})
            except:
                pass

    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
