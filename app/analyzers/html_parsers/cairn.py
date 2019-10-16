from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.3917
def parse_cairn(soup):
    
    authors = []
    affiliations = []
    is_french = False
    author_elts = soup.find_all(class_="auteur")

    for author_elt in author_elts:

#        if 'search-link' in author_elt.attrs['class']:
#            continue

        author={}
        structure_name, email = "", ""

        name_elt = author_elt.find(class_='nom_auteur')
        if name_elt:
            full_name = name_elt.get_text()
            full_name = full_name.replace("\n", " ").replace("\t", " ").strip()
            author['full_name'] = " ".join(w for w in full_name.split(' ') if len(w)>0) 

        affiliation_elt = author_elt.find(class_="affiliation")
        if affiliation_elt:
            structure_name = affiliation_elt.get_text().replace("\n", " ").strip()
            author['affiliations_info'] = [{'structure_name':structure_name}]
            affiliations.append(structure_name)

        email_elt = author_elt.find(class_="courriel")
        if email_elt:
            email = email_elt.get_text().replace('.at.','@')
            author['email'] = email

        if re.search(fr_regex, structure_name.lower().replace('-',' ')) or re.search(fr_regex, email.lower()):
            is_french = True

        authors.append(author)


    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':affiliations}

        
