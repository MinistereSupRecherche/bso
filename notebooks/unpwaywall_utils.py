import requests
import pandas as pd

def get_upw_info(doi):
    r = requests.get("https://api.oadoi.org/v2/{}?email=unpaywall@impactstory.org".format(doi))
    try:
        res = r.json()
    except:
        return {}

    oa_type = 'closed'
    oa_locations = res.get('oa_locations', [])
    if len(oa_locations) > 0:
        locations = list(set([loc['host_type'] for loc in oa_locations]))
        locations.sort()
        oa_type = ";".join(locations)
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
            "publisher" : res.get("publisher")
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
