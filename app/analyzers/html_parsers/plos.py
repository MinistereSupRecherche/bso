from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1371
def parse_plos(soup):

    is_french = False
    authors = []
    affiliations = []

    author_list_elt = soup.find(class_='author-list')
    if author_list_elt is None:
        return {'authors_from_html':authors, 'affiliations_complete':affiliations,  'is_french':is_french}
    for elt in author_list_elt.find_all('li'):
        if elt.find(class_='author-name') is None:
            continue

        full_name = elt.find(class_='author-name').get_text()
        author = {}
        author['full_name'] = full_name.strip()
        author['affiliations_info'] = []
        authors.append(author)

        for sub_elt in elt.find_all('a'):
            if isinstance(sub_elt, bs4.element.Tag) and 'href' in sub_elt.attrs:
                if 'orcid' in sub_elt.attrs['href']:
                    orcid = sub_elt.attrs['href'].replace('http', 'https')
                    author['orcid'] = orcid
                elif 'mailto' in sub_elt.attrs['href']:
                    email = sub_elt.attrs['href'].replace('mailto:', '')
                    author['email'] = email
        #author['email'] = elt.find_all(class_='email')[2].get_text()

        for sub_elt in elt.find_all('p'):
            if isinstance(sub_elt, bs4.element.Tag) and 'id' in sub_elt.attrs \
            and 'authAffiliations' in sub_elt.attrs['id']:
                structure_name = sub_elt.get_text().replace('Affiliation','').strip()
                author['affiliations_info'].append({'structure_name':structure_name})
                affiliations.append(structure_name)
                if re.search(fr_regex, structure_name.lower()):
                    is_french = True

    return {'authors_from_html':authors, 'affiliations_complete':affiliations,  'is_french':is_french}

        
