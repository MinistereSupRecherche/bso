from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1155
def parse_hindawi(soup):

    is_french = False

    authors, affiliations =[], []

    for elt in soup.find_all(class_="author_gp"):
        try:
            structure_name = elt.find_next_siblings('p')[0].get_text().strip()
            affiliations.append(structure_name)
            if re.search(fr_regex, structure_name.lower()):
                is_french = True
        except:
            continue

    return {'authors_from_html':authors, 'affiliations_complete': affiliations,  'is_french':is_french}

        
