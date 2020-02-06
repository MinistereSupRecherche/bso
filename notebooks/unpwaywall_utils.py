import requests
import pandas as pd

def get_upw_info(doi):
    r = requests.get("https://api.oadoi.org/v2/{}?email=unpaywall@impactstory.org".format(doi))
    try:
        oa_type = 'closed'
        oa_locations = r.json().get('oa_locations', [])
        if len(oa_locations) > 0:
            locations = list(set([loc['host_type'] for loc in oa_locations]))
            locations.sort()
            oa_type = ";".join(locations)
        return oa_type
    except:
        return 'unknown'
    
def enrich_with_upw_status(df):
    df['oa_type'] = None
    nb_publis = len(df)
    print("{} publications".format(nb_publis))
    for row in df.itertuples():
        if row.Index % 50 == 0:
            print("{} %".format(round(100 * row.Index / nb_publis)), end=', ')
        df.at[row.Index, 'oa_type'] = get_upw_info(row.doi)
    return df
