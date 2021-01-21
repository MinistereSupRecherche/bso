import requests
import pandas as pd

def dedup_sort(x):
    y = list(set([e for e in x if e]))
    y.sort()
    return y

def get_upw_info(doi):
    r = requests.get("https://api.oadoi.org/v2/{}?email=unpaywall@impactstory.org".format(doi))
    try:
        res = r.json()
    except:
        return {}

    oa_loc = res.get('oa_locations', [])
    host_types, repositories = [], []

    # loop over the oa locations to detect all the host types and all the repositories
    for loc in oa_loc:
        if loc is None:
            continue
        host_type = loc.get('host_type')
        host_types.append(host_type)

        if host_type == 'repository':
            current_repo = loc['url'].split('/')[2]
            if current_repo == 'doi.org':
                continue
            if 'hal' in current_repo.lower():
                current_repo = 'HAL'
            repositories.append(current_repo)

    host_types = dedup_sort(host_types)
    repositories = dedup_sort(repositories)

    if len(host_types) > 0:
        oa_type = ";".join(host_types)
    else:
        oa_type = 'closed'

    repositories = ";".join(repositories)

    return {
            "oa_type": oa_type,
            "is_oa" : res.get('is_oa', False),
            "title": res.get('title'),
            "published_date" : res.get('published_date'),
            "published_year" : res.get('year'),
            "genre" : res.get("genre"),
            "journal_is_in_doaj": res.get("journal_is_in_doaj"),
            "journal_is_in_doaj" : res.get("journal_is_in_doaj"),
            "journal_issns" : res.get("journal_issns"),
            "journal_name" : res.get("journal_name"),
            "publisher" : res.get("publisher"),
            "repositories" : repositories
            }
    
def enrich_with_upw_status(df):

    if 'doi' not in df:
        print("The input dataframe should have a column named 'doi'.")
        return df

    nb_publis = len(df)
    print("{} publications".format(nb_publis))
    for row in df.itertuples():
        if row.Index % 50 == 0:
            print("{} %".format(round(100 * row.Index / nb_publis)), end=', ')
        upw_info = get_upw_info(row.doi)
        for field in upw_info:
            df.at[row.Index, field] = upw_info[field]
    return df
