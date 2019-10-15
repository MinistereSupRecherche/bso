from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.3233
def parse_ios(soup):

    is_french = False

    authors, affiliations =[], []

    for elt in soup.find_all(class_='metadata-entry'):
        if ("affiliation" in elt.get_text().lower()):
            structure_name = elt.get_text().strip()
            if len(structure_name) > 0:
                affiliations.append(structure_name)
                if re.search(fr_regex, structure_name.lower()):
                    is_french = True

    return {'authors_from_html':authors, 'affiliations_complete': affiliations,  'is_french':is_french}

        
