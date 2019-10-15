from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1093
def parse_oup(soup):

    is_french = False

    authors, affiliations =[], []
    for elt in soup.find_all('div', {'id' : 'authorInfo_OUP_ArticleTop_Info_Widget'}):
        try:
            full_name = elt.find(class_='info-card-name').get_text()
            author = {}
            author['full_name'] = full_name
            author['affiliations_info'] = []
            authors.append(author)

            for aff in elt.find_all(class_='aff'):
                structure_name = aff.get_text().strip()
                author['affiliations_info'].append({'structure_name':structure_name})
                affiliations.append(structure_name)
                if re.search(fr_regex, structure_name.lower()):
                    is_french = True
        except:
            continue

    return {'authors_from_html':authors, 'affiliations_complete': affiliations,  'is_french':is_french}

        
