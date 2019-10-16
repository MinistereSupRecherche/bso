from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1021
def parse_acs(soup):
    is_french = False

    affiliations = {}
    for aff_elt in soup.find_all('div', {'id':re.compile('aff.')}):
        structure_name = ''
        sup_nb = 0
        for e in aff_elt.children:
            if e.name=='sup':
                sup_nb = e.get_text()
            elif isinstance(e, bs4.element.Tag):
                structure_name += ' ' + e.get_text().strip()
            else:
                structure_name += " ".join([w for w in e.replace("\n", " ").replace("\t", " ").strip().split(" ") if len(w)>0]).strip()
            if len(structure_name)>2:
                affiliations[sup_nb] = structure_name
                if re.search(fr_regex, structure_name.lower()):
                    is_french = True

    authors_name = {}
    authors = []

    for author_elt in soup.find_all(class_="hlFld-ContribAuthor"):

        author = {}
        author['affiliations_info'] = []
        full_name = ''

        try:
            full_name = author_elt.find('a').get_text()
            author['full_name'] = full_name
        except:
            continue

        for aff_elt in author_elt.find_all('sup'):
            aff_id = aff_elt.get_text()
            if aff_id in affiliations:
                author['affiliations_info'].append({'structure_name' : affiliations[aff_id]})
        if len(affiliations) == 1 and '0' in affiliations:
            author['affiliations_info'].append({'structure_name' : affiliations[0]})

        orcid_elt = author_elt.find(class_="orcid-link-icon")
        if orcid_elt:
            try:
                id_orcid = orcid_elt.find('a').attrs['href'].replace('http', 'https')
                author['orcid'] = id_orcid
            except:
                pass

        if full_name not in authors_name:
            authors.append(author)
            authors_name[full_name] = 1

    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
