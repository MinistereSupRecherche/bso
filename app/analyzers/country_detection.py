"""Detection of country for authors affiliations."""
import re
from app.config import BaseConfig
# import os
import requests
import json
from typing import Union, List, Any
from app.utils.logger import create_logger

logger = create_logger(__name__)


def construct_regex(a_list: List) -> Any:
    """Construct a regex."""
    return re.compile(
        '|'.join(["(?<![a-z])" + kw + "(?![a-z])" for kw in a_list])
    )


france_keywords = [
    'france', 'paris', 'lyon', 'marseille',
    'nantes', 'strasbourg', 'montpellier', 'cnrs',
    'perpignan', 'bordeaux', 'lille', 'limoges',
    'rouen', 'cergy', 'toulouse', 'versailles',
    'clermont', ' cedex', 'cedex ', 'amiens',
    'besancon', 'besançon',  'caen', 'corse', 'creteil',
    'créteil',  'dijon ', 'grenoble ', 'guadeloupe ',
    'sorbonne', 'avignon', 'vaucluse', 'la réunion', 'guyane',
    'guyana', 'mayotte', 'martinique', 'nancy', 'orléans',  'metz',
    'poitiers', 'reims', 'rennes', 'brest', 'picardie', 'noumea', 'nouméa',
    'new caledonia', 'aix', 'tours', 'marne', 'pau', 'adour', 'nice',
    'sophia-antipolis', 'inria', 'inserm', 'inra', 'ifsttar', 'brgm',
    'ifremer', 'onera', 'saclay', 'bourgogne', 'nancy 2', 'calédonie',
    'bretagne', 'savoie', 'toulon', 'umr', 'ehess', 'lorraine', 'panthéon',
    'univ-smb', 'mnhn.fr', 'collège de france', 'paristech', 'insee.fr',
    'iepg.fr', 'enpjj', 'rnsr'
]

fr_regex = construct_regex(france_keywords)


def keep_digits(x: str) -> str:
    """Delete all digit from a string."""
    return "".join([c for c in x if c.isdigit()]).strip()


def find_docid_hal(x: str) -> Union[None, str]:
    """Find the docid from input string."""
    try:
        for w in x.split(' '):
            if 'docid_hal_' in w:
                return w.split('_')[2].split(';')[0]
        return None
    except Exception:
        return None


def get_country_from_hal(docid) -> str:
    """Get country for a docid."""
    url = BaseConfig.HAL_URL_STRUCTURE\
        + "?q=docid:{}&fl=country_s".format(docid)
    r = requests.get(url)
    try:
        r = requests.get(url, timeout=2)
        if 'fr' == json.loads(r.text)['response']['docs'][0]['country_s']:
            return 'France'
        else:
            return json.loads(r.text)['response']['docs'][0]['country_s']
    except Exception:
        logger.debug("error in hal getting country for docid {}".format(docid))
        return 'unknown'
