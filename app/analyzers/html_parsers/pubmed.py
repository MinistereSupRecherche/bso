from bs4 import *
import re, bs4
from doi_utils import *

def parse_pubmed(soup):

    is_french = False

    aff_id, aff_name = None, None
    affiliations = {}
    if soup.find(class_="afflist") is not None:
        elt_to_use = []
        if soup.find(class_="afflist").find(class_="ui-ncbi-toggler-slave-open") is not None:
            elt_to_use = soup.find(class_="afflist").find(class_="ui-ncbi-toggler-slave-open").children
        elif soup.find(class_="afflist").find(class_="ui-ncbi-toggler-slave") is not None:
            elt_to_use = soup.find(class_="afflist").find(class_="ui-ncbi-toggler-slave").children

        for e in elt_to_use:
            if e.name == 'dt':
                aff_id = e.text.replace(',','')
            elif e.name == 'dd':
                aff_name = e.text
                if re.search(fr_regex, aff_name.lower()):
                    is_french = True

            if aff_id and aff_name:
                affiliations[aff_id] = aff_name

    current_author = {}
    authors = []
    if soup.find(class_="auths") is not None:
        for e in soup.find(class_="auths").children:
            if e.name == 'a':
                full_name = e.text
                if "full_name" in current_author:
                    authors.append(current_author)
                current_author = {"full_name": full_name}
                current_affiliations = []
                current_author['affiliations_info'] = current_affiliations

            elif e.name =="sup":
                aff_id = e.text.replace(',','')
                if aff_id in affiliations:
                    current_affiliation = {'structure_name':affiliations[aff_id]}
                    current_affiliations.append(current_affiliation)
        if "full_name" in current_author:
            authors.append(current_author)

    if len(affiliations) == 0 and len(soup.find_all(class_='fm-affl')) > 0:
        for aff in soup.find_all(class_='fm-affl'):
            aff_text = aff.text
            aff_name = aff_text[1:]
            affiliations[aff_text[0]] = aff_name
            if re.search(fr_regex, aff_name.lower()):
                is_french = True

    return {'authors_from_html': authors, 'affiliations_complete': [affiliations[a] for a in affiliations],  'is_french': is_french}

def parse_pubmed_api(soup):
        
    is_french = False
    authors = []
    affiliations = []
    
    for aut in soup.find_all('author'):
        author = {}
        last_name = aut.find('lastname')
        first_name = aut.find('forename')
        if last_name:
            author['last_name'] = last_name.text
        if first_name:
            author['first_name'] = first_name.text
        if len(author) > 0 and author not in authors:
            authors.append(author)
        author_aff = []
        for aff in aut.find_all('affiliation'):
            aff_name = aff.text
            if aff_name not in affiliations:
                affiliations.append(aff_name)
                if re.search(fr_regex, aff_name.lower()):
                    is_french = True
            author_aff.append({'structure_name': aff_name})
        if len(author_aff) > 0:
            author['affiliations_info'] = author_aff

    keywords = [k.text for k in soup.find_all('keyword')]
    pubmed_id_elt = soup.find('articleid', {'idtype':"pubmed"})
    if pubmed_id_elt:
        pubmed_id = pubmed_id_elt.text
        external_ids = [{'id_type': 'pubmed', 'id_value':pubmed_id}]
    return {'authors_from_html': authors, 'affiliations_complete': affiliations,  'is_french': is_french, 'keywords':keywords, 'id_external':external_ids}
