import requests
import pandas as pd

SCANR_API_BASE = "https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/"
def get_parents(structure_id):
    url = SCANR_API_BASE+"structures/search"
    params = {
        "filters": {
            "parents.structure.id": {
                "type":"MultiValueSearchFilter","op":"all","values":[structure_id]
            }
        },
        "sourceFields":["id"],
        "pageSize":10000
    }
    r = requests.post(url, json=params)
    res = r.json()['results']
    return [i['value']['id'] for i in res]

def get_supervised(structure_id):
    url = SCANR_API_BASE+"structures/search"
    params = {
        "filters": {
            "institutions.structure.id": {
                "type":"MultiValueSearchFilter","op":"all","values":[structure_id]
            }
        },
        "sourceFields":["id"],
        "pageSize":10000
    }
    r = requests.post(url, json=params)
    res = r.json()['results']
    return [i['value']['id'] for i in res]

def get_all_structures(structure_id, verbose = False):
    all_structures = [structure_id] + get_parents(structure_id) + get_supervised(structure_id)
    all_structures_dedup = list(set(all_structures))
    if verbose:
        print("Structures identifiées dans le périmètre : \n {}".format(", ".join(all_structures_dedup)))
    return all_structures_dedup

def get_publications_one_year(structure, year_start, verbose = False):
    structures = get_all_structures(structure, verbose)
    url = SCANR_API_BASE+"publications/search"
    params = {"pageSize":10000,
              "query":"","sort":{"year":"DESC"},"sourceFields":["id","title","year"],"filters":{"year":{"type":"LongRangeFilter","max":year_start + 1,"min":year_start,"missing":False},"productionType":{"type":"MultiValueSearchFilter","op":"all","values":["publication"]},"affiliations.id":{"type":"MultiValueSearchFilter","op":"any","values":
    structures
    }},"aggregations":{"types":{"field":"type","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":50},"productionTypes":{"field":"productionType","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":100},"keywordsEn":{"field":"keywords.en","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":100},"keywordsFr":{"field":"keywords.fr","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":100},"journal":{"field":"source.title","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":10},"years":{"field":"year","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":100},"isOa":{"field":"isOa","filters":{},"min_doc_count":1,"order":{"direction":"DESC","type":"COUNT"},"size":10}}}
    r = requests.post(url, json=params)
    if r.json()['total'] > 10000:
        print("Attention, plus de 10 000 publications. Seules 10 000 sont renvoyées par l'API.")
    if verbose:
        print("{} publications pour l'année {}".format(r.json()['total'], year_start), end=' ')
    res = r.json()['results']
    publi_with_doi = []
    for p in res:
        if 'doi' in p['value']['id']:
            p['value']['doi'] = p['value']['id'].replace('doi','')
            del p['value']['id']
            p['value']['title'] = p['value']['title']['default']
            if 'isOa' in p['value']:
                del p['value']['isOa']
            publi_with_doi.append(p['value'])       
    if verbose:
        print("dont {} avec un DOI".format(len(publi_with_doi)))
    return pd.DataFrame(publi_with_doi)

def get_publications_with_doi(structure, verbose = False):
    dfs = []
    for year in range(2013,2021):
        dfs.append(get_publications_one_year(structure, year, verbose))
    df = pd.concat(dfs)
    df = df.sort_values(by='year').reset_index()
    del df['index']
    return df
    
