from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1103
def parse_aps(soup):

    is_french = False

    authors, affiliations = [], {}
    is_french = False

    affiliations = {}
    for elt in soup.find_all(class_='authors'):
        for aff_elt in elt.find_all('li'):
            aff_id=0
            for sub_aff_elt in aff_elt.children:
                if isinstance(sub_aff_elt, bs4.element.Tag) and sub_aff_elt.name=='sup':
                    aff_id = sub_aff_elt.get_text()
                else:
                    info = sub_aff_elt
                    if info is not None:
                        if isinstance(info, bs4.element.Tag):
                            info = info.get_text()
                        affiliations[aff_id] = info
                        if re.search(fr_regex, info.lower()):
                            is_french = True

    author = None
    for elt in soup.find_all(class_='authors'):
        for sub_elt in elt.children:
            if isinstance(sub_elt, bs4.element.Tag):
                for sub_sub_elt in sub_elt.children:
                    if isinstance(sub_sub_elt, bs4.element.Tag):
                        for sub_sub_sub_elt in sub_sub_elt.children:
                            if isinstance(sub_sub_sub_elt, bs4.element.Tag):
                                if 'href' in (sub_sub_sub_elt.attrs):
                                    full_name = sub_sub_sub_elt.get_text()
    
                                    author = {}
                                    author['affiliations_info'] = []
                                    author['full_name'] = full_name
                                    
                                    authors.append(author)
                                    
                                if sub_sub_sub_elt.name == 'sup':
                                    nb_sups = sub_sub_sub_elt.get_text()
                                    for nb_sup in nb_sups.split(','):
                                        if nb_sup in affiliations:
                                            info = affiliations[nb_sup]
                                            if '@' in info:
                                                author['email'] = info
                                            else:
                                                author['affiliations_info'].append({'structure_name':info})


    return {'authors_from_html':authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french':is_french}

        
