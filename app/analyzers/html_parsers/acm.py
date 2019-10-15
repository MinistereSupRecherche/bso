from bs4 import *
import re, bs4
from doi_utils import *

def parse_acm(soup):

    is_french = False

    authors = []
    affiliations = []

    authors_table = None
    for k in soup.find_all('table'):
        if 'Authors:' in k.get_text() or 'Author:' in k.get_text():
            authors_table = k.find_all('table')[0]
            break
    
    if authors_table:
        for tr in authors_table.find_all('tr'):
            if tr.find('table'):
                continue

            full_name, aff_name = None, None
            author = {}
            for e in tr.find_all('a'):
                if e.attrs.get('title') == "Author Profile Page":
                    full_name = e.text
                    author['full_name'] = full_name
                if e.attrs.get('title') == "Institutional Profile Page":
                    aff_name = e.text
                    author['affiliations_info'] = [{'structure_name': aff_name}]
                    if aff_name not in affiliations:
                        affiliations.append(aff_name)


            for e in tr.find_all('small'):
                aff_name = e.text
                if aff_name not in affiliations:
                    affiliations.append(aff_name)

                if 'affiliations_info' not in author:
                    author['affiliations_info'] = []

                if {'structure_name': aff_name} not in author['affiliations_info']:
                    author['affiliations_info'].append({'structure_name': aff_name})
            if len(author) > 0 and author not in authors:
                authors.append(author)

    for aff_name in affiliations:
        if re.search(fr_regex, aff_name.lower()):
            is_french = True

    return {'authors_from_html': authors, 'affiliations_complete': affiliations,  'is_french': is_french}

        
