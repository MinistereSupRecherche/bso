import copy
from bs4 import BeautifulSoup
from doi_utils import *

# doi 10.1038
def parse_nature(soup):

    list_authors = soup.find(class_='js-list-authors')

    authors = []
    affiliations = {}

    if(list_authors == None):
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

    is_french = False

    for elt in list_authors.find_all(itemprop="author"):
        author = {}
        name_elt = elt.find('span', itemprop="name")
        if(name_elt):
            author['full_name'] = name_elt.get_text()

        author['affiliations_info'] = []
        for k in elt.find_all(itemprop="affiliation"):
            affiliation={}
            structure_name = ""
            for info_type in ['address', 'name']:
                value_elt = k.find(itemprop=info_type)
                if(value_elt and 'content' in value_elt.attrs):
                    #affiliation[info_type] = value_elt.attrs['content']
                    structure_name += value_elt.attrs['content']+";"
            affiliation['structure_name'] = structure_name
            if re.search(fr_regex, structure_name.lower().replace('-',' ')):
                is_french = True

            author['affiliations_info'].append(copy.deepcopy(affiliation))

        if 'full_name' in author:
            authors.append(author)

 
    return {'is_french':is_french, 'authors_from_html':authors, 'affiliations_complete':affiliations}

