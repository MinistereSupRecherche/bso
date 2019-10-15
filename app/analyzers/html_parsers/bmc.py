from bs4 import BeautifulSoup
import re
from doi_utils import *


# doi 10.1186

def parse_bmc(soup):
    authors = []
    affiliations_complete= []

    is_french = False
    author_elts = soup.find_all(class_="hasAffil")
    if author_elts is None:
        return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':affiliations_complete}

    authors = []
    affiliations = {}
    for aff_elt in soup.find_all(class_="Affiliation"):
        try:
            aff_id = aff_elt.attrs['id']
            structure_name = aff_elt.get_text().strip()
            affiliations[aff_id] = structure_name.replace(u'\xa0', u' ')
            
            if re.search(fr_regex, structure_name.lower()) or  re.search(fr_regex, email.lower()):
                is_french = True
        except:
            pass

    
    for e in soup.find_all(class_="hasAffil"):

        author ={}
        author['affiliations_info'] = []
        full_name, email = None, None
        try:
            full_name = e.find(class_="AuthorName").get_text()
        except:
            pass
        try:
            email = e.find(class_="EmailAuthor").attrs['href'].replace('mailto:','')
        except:
            pass
    
        if full_name:
            author['full_name'] = full_name.replace(u'\xa0', u' ')
        if email:
            author['email'] = email
        
        for a in e.find_all(class_="AffiliationID"):
            aff_id = a.attrs['href'].replace("#",'')
            if aff_id in affiliations:
                author['affiliations_info'].append({'structure_name': affiliations[aff_id]})
            
        authors.append(author)

    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete': [affiliations[a] for a in affiliations]}

