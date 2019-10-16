from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1080
def parse_tandf(soup):
    
    authors = []
    affiliations = []

    is_french = False
    author_elts = soup.find_all(class_="entryAuthor")

    for author_elt in author_elts:

        if 'search-link' in author_elt.attrs['class']:
            continue

        author={}
        structure_name, email = "", ""

        for e in author_elt.children:
            if(isinstance(e, bs4.element.NavigableString)):
                full_name = e
                author['full_name'] = full_name
            if(isinstance(e, bs4.element.Tag)):
                for sub_e in e.children:
                    if(isinstance(sub_e, bs4.element.NavigableString)):
                        structure_name = sub_e
                        author['affiliations_info'] = [{'structure_name':structure_name}]
                        affiliations.append(structure_name)

        email_elt = author_elt.find(class_="corr-email")
        if email_elt:
            email = email_elt.get_text()
            author['email'] = email

        if re.search(fr_regex, structure_name.lower()) or re.search(fr_regex, email.lower()):
            is_french = True

        if len(author) > 0 and author not in authors:
            authors.append(author)


    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':affiliations}

        
