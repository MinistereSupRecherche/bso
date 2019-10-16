from doi_utils import *
from generic import *
import json, copy

#doi 10.1016

def parse_elsevier(a_publication, soup):

    try:
        html = a_publication.landing_page_html
    except:
        html = a_publication
    if html in ['not_downloaded', 'error_ip_blocked', 'error', 'AVOID']:
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

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
        return {'is_french': is_french, 'authors_from_html':authors, 'affiliations_complete':affiliations, 'affiliations_fr':affiliations_fr}

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
                        info_content = aff[i]['_']

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
                    info_content = elt[k]['_']

                    if info_type not in affiliation:
                            affiliation[info_type] = []

                    affiliation[info_type].append(info_content)

                    if re.search(fr_regex, info_content.lower()):
                                is_french = True
        if(affiliation):              
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
                if 'country' in aff_c:
                    aff['country'] = aff_c['country']
            author['affiliations_info'] = new_affiliations_info


    return {'is_french': is_french, 'authors_from_html':authors, 'affiliations_complete':affiliations, 'affiliations_fr':affiliations_fr}

