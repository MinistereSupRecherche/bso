import re
from typing import List, Union, Dict

def obj_to_str(obj: Union[Dict,str]) -> str:
    ans = ""

    if isinstance(obj,str):
        return obj

    if isinstance(obj, dict):
        for field in obj:
            if obj[field] and isinstance(obj[field], str):
                value = obj[field].strip()+';'
            elif obj[field]:
                value = obj_to_str(obj[field]).strip()

            if len(value)>0:
                ans += value.replace(';;',';')
        return ans
    
    if isinstance(obj, list):
        for e in obj:
            value = obj_to_str(e).strip()+';'
            if len(value)>0:
                ans += value.replace(';;',';')
        return ans


def construct_regex(a_list):
    return re.compile('|'.join(["(?<![a-z])" + kw + "(?![a-z])" for kw in a_list]))

france_keywords = ['france', 'paris', 'lyon', 'marseille', 'nantes', 'strasbourg', 'montpellier', 'cnrs',\
'perpignan', 'bordeaux', 'lille', 'limoges', 'rouen', 'cergy', 'toulouse', 'versailles', 'clermont', \
' cedex', 'cedex ', 'amiens', 'besancon', 'besançon',  'caen', 'corse', 'creteil', 'créteil',  \
'dijon ', 'grenoble ', 'guadeloupe ', 'sorbonne', 'avignon', 'vaucluse', 'la réunion', \
'guyane', 'french guyana', 'mayotte', 'martinique', 'nancy', 'orléans',  'metz', 'poitiers', 'reims', 'rennes', 'brest', \
'picardie', 'noumea', 'nouméa', 'new caledonia', 'aix', 'tours', 'marne', 'pau', 'adour', 'nice', 'sophia-antipolis', \
'inria', 'inserm', 'inra', 'ifsttar', 'brgm', 'ifremer', 'onera', 'saclay', 'bourgogne', 'nancy 2', 'calédonie', \
'bretagne', 'savoie', 'toulon', 'umr', 'ehess', 'lorraine', 'panthéon','univ-smb', 'mnhn.fr', 'collège de france', 'paristech', \
'insee.fr', 'iepg.fr', 'enpjj', 'picardy', 'azur', 'kedge']

fr_regex = construct_regex(france_keywords)

def keep_digits(x):
    return "".join([c for c in x if c.isdigit()]).strip()
