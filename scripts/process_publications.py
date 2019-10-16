import requests
import math
import datetime
from joblib import Parallel, delayed

APP_URL = "http://0.0.0.0:5000/publications"
APP_URL_DATA = "http://0.0.0.0:5000/publications"
YEAR_START = 2013
YEAR_END = 2013
header = {'Authorization': 'Basic YWRtaW46ZGF0YUVTUjIwMTk='}
NB_JOBS = 10  # nb jobs in parrallel


def update_unpaywall_dump(elt, etag):
    """ Set treated flag to true in unpaywll_dump collection """
    # url_unpaywall_dump = APP_URL + "/dumps_unpaywall/{}".format(elt['doi'])
    url_unpaywall_dump = APP_URL_DATA
    url_unpaywall_dump += "/dumps/unpaywall/{}".format(elt['doi'])
    headers_update = header.copy()
    headers_update['If-Match'] = etag

    elt['treated'] = True

    r = requests.patch(url_unpaywall_dump, headers=headers_update, json=elt)
    if r.ok is False:
        print("MAJ unpaywall_dump ERREUR pour le doi {}".format(elt['doi']))
        # print(r.text)


def process_doi_unpaywall(elt):

    etag = elt['etag']

    # remove datastore fields
    for field in ['modified_at', 'created_at', '_id', 'etag']:
        if field in elt:
            del elt[field]
    # send data to analyzer unpaywall service
    url_unpaywall_publi = APP_URL + "/analyzers/unpaywall_publication"
    r = requests.post(url_unpaywall_publi, json=elt, headers=header)
    if r.ok is False:
        print("MAJ publication ERREUR pour le doi {}".format(elt['doi']))
        # print(r.text)

    # update unpaywall dump collection (setting treated flag to True)
    update_unpaywall_dump(elt, etag)


def keep_updating(year):
    NB_ELT = 1000
    j = 0
    url = APP_URL_DATA + "/dumps/unpaywall/?where={\"treated\":false,\"year\":"
    url += str(year) + "}&max_results=" + str(NB_ELT) + "&page="+str(j)
    r = requests.get(url, headers=header)
    nb_elts = r.json()['meta']['total']
    nb_pages = math.ceil(nb_elts/NB_ELT)
    print("Still {} pages to process for year {}".format(nb_pages, year))

    return {'nb_pages': nb_pages, 'data': r.json()['data']}


def process_year(year):
    should_keep_updating = keep_updating(year)
    max_iter = should_keep_updating['nb_pages'] + 2
    nb_iter = 0
    while ((should_keep_updating['nb_pages'] > 0) and (nb_iter < max_iter)):
        start_time = datetime.datetime.now()
        Parallel(n_jobs=NB_JOBS)(delayed(
            process_doi_unpaywall)(
                elt) for elt in should_keep_updating['data'])
        end_time = datetime.datetime.now()
        print("{}: {}".format(
            should_keep_updating['nb_pages'], end_time-start_time), end=" -- ")
        should_keep_updating = keep_updating(year)
        nb_iter += 1


def test():
    url = APP_URL_DATA + "/dumps/unpaywall/?where={\"doi\":\""
    url += "10.4000/rechercheformation.2839\",\"treated\":false}"
    try:
        test_json = requests.get(url, headers=header).json()['data'][0]
        print(test_json)
    except Exception:
        print("The test element is not in the unpaywall dump collection \
                or it has already be processed")
        return
    process_doi_unpaywall(test_json)


# test()
for year in range(YEAR_START, YEAR_END + 1):
    process_year(year)
