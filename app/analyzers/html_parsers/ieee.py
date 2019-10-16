from bs4 import *
import re, bs4, json
from doi_utils import *

def parse_ieee(soup):

    is_french = False

    for s in soup.find_all('script'):
        if "global.document.metadata" in s.get_text():
            break

    infos = re.sub(".*global.document.metadata=", "", s.text.replace("\n", " ")).strip().replace("};","}")
    authors = []
    affiliations = []
    for a in json.loads(infos).get('authors', []):
        author = {}
        if "firstName" in a:
            author['first_name'] = a['firstName']
        if "lastName" in a:
            author['last_name'] = a['lastName']
        if "affiliation" in a:
            author['affiliations_info'] = []
            aff_name = BeautifulSoup(a["affiliation"], 'lxml').text
            if aff_name not in affiliations:
                affiliations.append(aff_name)
                if re.search(fr_regex, aff_name.lower()):
                    is_french = True
            author['affiliations_info'].append({"structure_name": aff_name})
        authors.append(author)

    return {'authors_from_html': authors, 'affiliations_complete': affiliations,  'is_french': is_french}

        
