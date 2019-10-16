from bs4 import *
import re, bs4
from doi_utils import *


# doi 10.1051
def parse_aanda(soup):
    
    authors, affiliations = [], {}
    is_french = False

    affiliations = {}
    sup_nb = 0
    structure_name = ''

    aff_class_elt = soup.find(class_ = 'aff')
    if aff_class_elt is None:
        return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':[affiliations[sup] for sup in affiliations]}

    for aff_elt in aff_class_elt.children:

        if aff_elt.name=='sup':
            structure_name = ''
            sup_nb = aff_elt.get_text()
        elif isinstance(aff_elt, bs4.element.Tag):
            structure_name += ' ' + aff_elt.get_text().strip()
        else:
            info = " ".join([w for w in aff_elt.replace("\n", " ").replace("\t", " ").strip().split(" ") if len(w)>0])
            if 'e-mail' in info:
                email = info
            else:
                structure_name += info
                affiliations[sup_nb] = structure_name
            if re.search(fr_regex, info.lower().replace('-',' ')):
                is_french = True

    author = None

    try:
        for elt in soup.find(class_='article-authors').children:
            for sub_elt in elt.children:

                if isinstance(sub_elt, bs4.element.Tag):
                    if sub_elt.attrs and 'class' in sub_elt.attrs and 'author' in sub_elt.attrs['class']:
                        full_name = sub_elt.get_text()
                        if author:
                            authors.append(author)
                        author = {}
                        author['full_name'] = full_name
                        author['affiliations_info'] = []
                
                    if sub_elt.name=='sup':
                        sup_nb  = keep_digits(sub_elt.get_text())
                        if sup_nb in affiliations:
                            author['affiliations_info'].append({'structure_name': affiliations[sup_nb]})
    except:
        pass

    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':[affiliations[sup] for sup in affiliations]}

        
