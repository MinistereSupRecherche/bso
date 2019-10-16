from bs4 import BeautifulSoup
import re
from doi_utils import *

#doi 10.1007

def parse_springer(soup):

    #info = soup.find(class_='authors__affiliations')
    info = soup.find(class_='authors-affiliations')
    
    affiliations = {}
    authors = []
    
    if info==None:
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}
   
    contributor_names = info.find(class_="test-contributor-names")
    affiliations_names = info.find(class_="test-affiliations")

    if (affiliations_names is None) or (contributor_names is None):
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

    is_french = False
    
    
    for elt in affiliations_names.find_all('li', itemtype="http://schema.org/Organization"):
        affiliation_id = elt.attrs['data-test']
        current_affiliation = {}
        structure_name = ''
        for info_type in ['name', 'addressRegion', 'addressCountry', 'department']:
            value_elt = elt.find(itemprop=info_type)
            if(value_elt):
                #current_affiliation[info_type] = value_elt.get_text()
                if info_type=='addressCountry':
                    current_affiliation['country'] = value_elt.get_text()
                structure_name += value_elt.get_text()+';'
                if re.search(fr_regex, value_elt.get_text().lower()):
                    is_french = True
        current_affiliation['structure_name'] = structure_name
                    
        affiliations[affiliation_id] = current_affiliation
        
    
    for elt in contributor_names.find_all('li', itemtype="http://schema.org/Person"):

        if elt is None:
            continue
        author={}
        #print(elt)
        name = None
        name_elt = elt.find(itemprop='name')
        if (name_elt):
            name = name_elt.get_text()
            author['full_name'] = name

        email_elt =  elt.find(itemprop='email')    
        if (email_elt and 'href' in email_elt.attrs):
            author['email'] = email_elt.attrs['href'].replace('mailto:','')

        #author['affiliations_id'] = []
        author['affiliations_info'] = []
        for k in elt.find_all('li', {'data-affiliation':True}):
            affiliation_id = k.attrs['data-affiliation']
            #author['affiliations_id'].append(affiliation_id)
            if affiliation_id in affiliations:
                author['affiliations_info'].append(affiliations[affiliation_id])

        orcid_elt = elt.find(class_='gtm-orcid-link')
        if(orcid_elt and 'href' in orcid_elt.attrs):
            author['orcid'] = orcid_elt.attrs['href']

        if 'full_name' in author:
            authors.append(author)
            
    return {'is_french':is_french, 'authors_from_html':authors, 'affiliations_complete':[affiliations[a] for a in affiliations]}

