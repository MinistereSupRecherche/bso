from bs4 import BeautifulSoup
import re
from doi_utils import *


# doi 10.1002, 10.1111
def parse_wiley(soup):
    
    authors = []
    affiliations = []

    is_french = False
    author_elts = soup.find_all(class_="accordion__closed")

    for author_elt in author_elts:
        author={}
        author_name = author_elt.find(class_='author-name')
        author['full_name'] = author_name.get_text()

        for author_info in author_elt.find_all(class_='author-info'):


            author['affiliations_info']=[]
            orcid = author_info.find(class_ = 'orcid-account')
            if orcid:
                author['orcid'] = orcid.get_text().replace('http','https')

            for elt in author_info.find_all('p'):
                if elt.attrs=={} and 'mail' not in elt.get_text().lower() and len(elt.get_text())>4 and elt.get_text().lower() not in [ author_name.get_text().lower(), 'correspondence']:
                    author['affiliations_info'].append({'structure_name':elt.get_text()})
                    affiliations.append(elt.get_text())
                    if re.search(fr_regex, elt.get_text().lower()):
                        is_french = True

            for elt in author_info.find_all('a'):
                if 'href' in elt.attrs and 'mailto' in elt.attrs['href']:
                    email = elt.attrs['href'].replace('mailto:','').replace('%E2%80%90','@')
                    author['email']=email
                    if re.search(fr_regex, email.lower()):
                        is_french = True

            if author not in authors:
                authors.append(author)

    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':affiliations}

        
