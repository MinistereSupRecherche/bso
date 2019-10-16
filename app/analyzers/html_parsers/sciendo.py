from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1515
def parse_sciendo(soup):

    is_french = False

    authors, affiliations =[], []

    potential_elts = []

    for kw in ['affiliation', 'affiliations', 'aff-overlay', 'author-tooltip-affiliation','morearticleinfo', 'author-info',\
            'author-tooltip-affiliation', 'author-affiliation', 'authorAffiliation', 'contentContribs', 'expandable-author', \
            'PublicationsDetailBold', 'aff', 'org', 'content-header__institution', 'article-author-affilitation']:
        for elt in soup.find_all(class_=kw):
            potential_elts.append(elt)

    for elt in soup.find_all('span', {'id':re.compile('affilia.*')}):
        potential_elts.append(elt)
    
    for elt in soup.find_all('div', {'id':re.compile('cAffi')}):
        potential_elts.append(elt)

    for elt in soup.find_all('div', {'id':re.compile('.*auteur.*')}):
        potential_elts.append(elt)
    
    for elt in potential_elts:
        structure_name = elt.get_text().strip()
        if len(structure_name) > 0:
            affiliations.append(structure_name)
            if re.search(fr_regex, structure_name.lower()):
                is_french = True

    return {'authors_from_html':authors, 'affiliations_complete': affiliations,  'is_french':is_french}

        
