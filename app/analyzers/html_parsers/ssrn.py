from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.2139
def parse_ssrn(soup):

    is_french = False

    authors, affiliations =[], []
    for kw in ['authors', 'article-author-affiliations']:
        if soup.find(class_=kw):
            for elt in soup.find(class_=kw).find_all('p'):

                structure_name = elt.get_text().strip()
                affiliations.append(structure_name)


                if re.search(fr_regex, structure_name.lower()):
                    is_french = True

    return {'authors_from_html':authors, 'affiliations_complete': affiliations,  'is_french':is_french}

        
