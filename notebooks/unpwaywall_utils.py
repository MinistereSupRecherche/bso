import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import pandas as pd


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def dedup_sort(x):
    y = list(set([e for e in x if e]))
    y.sort()
    return y

def get_upw_info(doi):
    if pd.isnull(doi):
        return {}
    try:
        r = requests_retry_session().get("https://api.oadoi.org/v2/{}?email=unpaywall@impactstory.org".format(doi))
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
            "journal_is_oa" : res.get("journal_is_oa"),
            "journal_issns" : res.get("journal_issns"),
            "journal_name" : res.get("journal_name"),
            "publisher" : res.get("publisher"),
            "repositories" : repositories
            }
    
def enrich_with_upw_status(df):

    if 'DOI' in df:
        df['doi'] = df['DOI']

    if 'doi' not in df:
        print("The input dataframe should have a column named 'doi'.")
        return df

    nb_publis = len(df)
    enriched_data = []
    print("{} publications".format(nb_publis))
    for ix, row in df.iterrows():
        if ix % 50 == 0:
            print("{} %".format(round(100 * ix / nb_publis)), end=', ')
        upw_info = get_upw_info(row.doi)
        enriched_data_elt = row.to_dict()
        enriched_data_elt.update(upw_info)
        enriched_data.append(enriched_data_elt)

    enriched_df = pd.DataFrame(enriched_data)
    return enriched_df
