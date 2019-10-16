import requests
import json

DATAESR_NOTICES = "http://0.0.0.0:5000/publications/notices_publications"


def post_notice(d):
    r = requests.post(DATAESR_NOTICES, json=d)
    if r.ok is False:
        print(r.text)


# loading an example of document, with 2 fields, id and notice
elt_example = json.load(open("html_example.json", "r"))

# loading this element into the db
post_notice(elt_example)
