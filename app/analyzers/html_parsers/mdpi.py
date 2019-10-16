from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.3390
def parse_mdpi(soup):

    is_french = False

    affiliations = {}
    authors = []
    for elt in soup.find_all(class_='affiliation'):
        try:
            nb_sup = elt.find(class_='affiliation-item').get_text()
        except:
            nb_sup = 0

        try:
            structure_name = elt.find(class_='affiliation-name').get_text().strip()
            affiliations[nb_sup] = structure_name
            if re.search(fr_regex, structure_name.lower()):
                is_french = True
        except:
            pass

    for elt in soup.find_all(class_='inlineblock'):
        try:    
            full_name = elt.find('a', {'itemprop':'author'}).get_text().strip()
            author = {}
            author['full_name'] = full_name
            author['affiliations_info'] =[]
            authors.append(author)
        except:
            continue
    
        if elt.find('sup'):
            sups = elt.find('sup').get_text().split(',')
            for sup in sups:
                sup = sup.strip()
                if sup in affiliations:
                    author['affiliations_info'].append({'structure_name': affiliations[sup]})

    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
