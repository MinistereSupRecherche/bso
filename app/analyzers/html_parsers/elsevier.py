from doi_utils import *
from generic import *
import json, copy

#doi 10.1016

def fallback(soup):
    is_french = False
    authors = []
    affiliations = []
    for elt in soup.find_all(class_ = 'author'):
        author = None
        last_name, first_name = None, None
        try:
            for sub_elt in elt.find_all('a'):
                if 'href' in sub_elt.attrs and 'authorLookUp' in sub_elt.attrs['href']:
                    full_name = sub_elt.attrs['href'].split('&')[1].split('=')[1]
                    last_name = full_name.split(',')[0].strip()
                    first_name = full_name.split(',')[1].strip()
        except:
            pass
        
        if last_name:
            author = {'last_name': last_name, 'affiliations_info': []}
        if first_name and author:
            author['first_name'] = first_name
        
        for aff_elt in elt.find_all(class_ = 'affiliations'):
            structure_name = aff_elt.get_text()
        
            if author:
                author['affiliations_info'].append({'structure_name': structure_name})
            affiliations.append(structure_name)
            if re.search(fr_regex, structure_name.lower()):
                is_french = True
        
        if author:
            authors.append(author)

    if len(affiliations) == 0:
        for elt in soup.find_all('meta', {'name':'citation_author_institution'}):
            if 'content' in elt.attrs:
                structure_name = elt.attrs['content']
                affiliations.append(structure_name)
                if re.search(fr_regex, structure_name.lower()):
                    is_french = True
    
    affiliations = list(set(affiliations))
    
    return {'is_french':is_french, 'affiliations_complete':affiliations, 'authors_from_html':authors}


def parse_elsevier(soup):

    is_french = None
    affiliations = {}
    authors = []
    affiliations_fr = []
    
    js = None


    try:
        for s in soup.find_all('script'):
            if ('type' in s.attrs) and (s.attrs['type']=='application/json'):
                js = json.loads(s.get_text())
                break
    except:
        pass

    if js==None or 'authors' not in js:
        return fallback(soup)

    is_french = False

    correspondences = {}
    for aff_id in js['authors']['correspondences']:
        elt = js['authors']['correspondences'][aff_id]['$$']
        for k in range(0, len(elt)):
            if elt[k]['#name'] == 'text' and '_' in elt[k]:
                aff = elt[k]['_']
                correspondences[aff_id]={'address': aff}




    for aff_id in js['authors']['affiliations']:
        affiliations[aff_id] = []

        elt = js['authors']['affiliations'][aff_id]['$$']
    
        affiliation = None
        for k in range(0, len(elt)):
            if elt[k]['#name'] == 'affiliation':
                aff = elt[k]['$$']

                affiliation = {}

                for i in range(0, len(aff)):

                    if '_' in aff[i]:
                        info_type = aff[i]['#name']
                        if info_type in ["address-line", "postal-code"]:
                            info_type = 'address'
                        elif info_type == 'organization':
                            info_type = 'institution_name'
                        info_content = str(aff[i]['_'])

                        if info_type not in affiliation:
                            affiliation[info_type] = []

                        affiliation[info_type].append(info_content)

                        if info_type=='country' and re.search(fr_regex, info_content.lower()):
                            is_french = True
                            
        if(affiliation==None):
            affiliation = {}
            for k in range(0, len(elt)):
                if elt[k]['#name'] == 'textfn' and '_' in elt[k] :

                    info_type = elt[k]['#name']
                    if info_type in ["address-line", "postal-code"]:
                        info_type = 'address'
                    elif info_type == 'organization':
                        info_type = 'institution_name'
                    info_content = str(elt[k]['_'])

                    if info_type not in affiliation:
                            affiliation[info_type] = []

                    affiliation[info_type].append(info_content)

                    if re.search(fr_regex, info_content.lower()):
                                is_french = True


        if(affiliation):              
            for field in affiliation:
                if isinstance(affiliation[field], list):
                    affiliation[field] = ";".join(affiliation[field])
            affiliations[aff_id].append(affiliation)

    


    for aut in js['authors']['content']:

        for elt in aut['$$']:

            if elt['#name']!='author':
                continue

            author = {}
            author['affiliations_info'] = []

            for i in elt['$$']:
                #if (i['#name'] in ['given-name', 'surname', 'e-address']) and '_' in i:
                #    author[i['#name']] = i['_']
                if (i['#name'] in ['given-name']) and '_' in i:
                    author['first_name'] = i['_']
                if i['#name'] == 'surname' and '_' in i:
                    author['last_name'] = i['_']
                if i['#name'] == 'e-address' and '_' in i:
                    author['email'] = i['_']
                #elif i['#name']=='affiliation':
                #    affiliation = {}
                #    for elt in i['$$']:
                #        info_type = elt['#name']
                #        info_content = elt['_']
                #        if info_type not in affiliation:
                #            affiliation[info_type] = []
                #            
                #        affiliation[info_type].append(info_content)
                #        
                #    author['affiliations'].append(affiliation)
                elif i['#name']=='cross-ref':
                    aff_id = i['$']['refid']
                    if aff_id in affiliations:
                        author['affiliations_info'].append(copy.deepcopy(affiliations[aff_id]))
                    if aff_id in correspondences:
                        author['affiliations_info'].append(copy.deepcopy(correspondences[aff_id]))
                        if 'address' in correspondences[aff_id] and ', france' in correspondences[aff_id]['address'].lower():
                            is_french = True

            if 'last_name' in author:
                authors.append(author)


    for key in affiliations:
        elts = affiliations[key]
        for elt in elts:
            if 'country' in elt and 'organization' in elt and 'France' in elt['country']:
                affiliations_fr += elt['organization']

    if len(affiliations) == 1: #all authors have the same affiliation
        for author in authors:
            author['affiliations_info'] += copy.deepcopy(affiliations[list(affiliations.keys())[0]])

    affiliations_complete = []
    for author in authors:
        if 'affiliations_info' in author:
            new_affiliations_info = []
            for aff in author['affiliations_info']:
                
                if isinstance(aff,list):
                    for e in aff:
                        new_affiliations_info.append(e)
                else:
                    new_affiliations_info.append(aff)

            for aff in new_affiliations_info:
                aff_c = aff.copy()
                aff['structure_name'] = obj_to_str(aff_c)

                fields = list(aff.keys())
                for field in fields:
                    if field not in ['structure_name', 'country', 'address', 'institution_name']:
                        del aff[field]

            author['affiliations_info'] = new_affiliations_info
            affiliations_complete += new_affiliations_info


    return {'is_french': is_french, 'authors_from_html':authors, 'affiliations_complete':affiliations_complete, 'affiliations_fr':affiliations_fr}

