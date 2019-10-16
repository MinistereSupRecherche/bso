import os
import re
import requests
import datetime
import json
from joblib import Parallel, delayed

DATA_PATH = "/media/jerem/DATA/Eric/OpenScience/unpaywall_test/"
UNPAYWALL_SNAPSHOT_BASE_URL = \
        "https://s3-us-west-2.amazonaws.com/unpaywall-data-snapshots/"
UNPAYWALL_SNAPSHOT_FILE = \
        "unpaywall_snapshot_2018-06-21T164548_with_versions.jsonl.gz"
UNPAYWALL_SNAPSHOT_URL = UNPAYWALL_SNAPSHOT_BASE_URL + UNPAYWALL_SNAPSHOT_FILE
DATAESR_UNPAYWALL_DUMP = "http://0.0.0.0:5000/publications/dumps_unpaywall"
YEAR_START = 2017
YEAR_END = 2017
NB_JOBS = 4  # nb jobs in parrallel


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def normalize_doi(doi):
    """ Remove / at the end of the doi and lower it """
    doi_normalized = re.sub("(/){1,}$", "", doi.lower())
    return doi_normalized


def post_unpaywall_data(d):
    d['doi'] = normalize_doi(d['doi'])
    d['treated'] = False
    r = requests.post(DATAESR_UNPAYWALL_DUMP, json=d)
    if r.ok is False:
        print(r.text)


download_snapshot = False
# download and unzip the unpaywall snapshot
if download_snapshot:
    os.system("mkdir -p {}".format(DATA_PATH))

    print("start downloading and unzipping data ")
    os.system("cd {0} && wget {1} && gunzip {2}".format(
        DATA_PATH, UNPAYWALL_SNAPSHOT_URL, UNPAYWALL_SNAPSHOT_FILE))
    print(" done !")
    print()

split_snapshot = False
# split by year
if split_snapshot:
    print("start filtering and splitting data ")
    for year in range(YEAR_START, YEAR_END + 1):
        os.system("mkdir -p {}{}".format(DATA_PATH, year))
        fgrep_cmd = 'fgrep "\\"year\\": {}" {}'.format(
                year, UNPAYWALL_SNAPSHOT_FILE.replace('.gz', ''))

        # keeping lines with the wanted year
        grep_year_cmd = "cd {} && ".format(DATA_PATH) + fgrep_cmd
        grep_year_cmd += " > {0}{1}/unpaywall_{1}.json".format(DATA_PATH, year)
        os.system(grep_year_cmd)

        # splitting the file
        split_cmd = "cd {0}{1} && split -l 100000 unpaywall_{1}.json".format(
                DATA_PATH, year)
        os.system(split_cmd)
    print(" done !")
    print()

# now loading the dump unpaywall data
for year in range(YEAR_START, YEAR_END + 1):
    files = []
    for x in os.listdir('{}{}'.format(DATA_PATH, year)):
        if len(x) == 3 and x[0] == 'x':
            files.append(x)
    files = sorted(files)

    for file_x in files:
        start_time = datetime.datetime.now()
        elts = []
        with open('{}{}/{}'.format(DATA_PATH, year, file_x)) as f:
            for line in f:
                elts.append(json.loads(line))

        elts_chunks = list(chunks(elts, 1000))
        for i, sub_list in enumerate(elts_chunks):
            Parallel(n_jobs=NB_JOBS)(
                    delayed(
                        post_unpaywall_data)(elt) for elt in sub_list)
        end_time = datetime.datetime.now()
        print("{} {}: {}".format(year, file_x, end_time - start_time))
