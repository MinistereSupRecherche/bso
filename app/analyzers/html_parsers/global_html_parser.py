from elsevier import *
from nature import *
from wiley import *
from springer import *
from openedition import *
from tandf import *
from cairn import *
from aanda import *
from acs import *
from bmc import *
from aps import *
from iop import *
from frontiers import *
from rsc import *
from plos import *
from cambridge import *
from mdpi import *
from oup import *
from aip import *
from spie import *
from atmos_chem import *
from bmj import *
from sagepub import *
from erudit import *
from ssrn import *
from sciendo import *
from hindawi import *
from ios import *
from pubmed import *
from ieee import *
from acm import *

from bs4 import BeautifulSoup

def is_empty(res):
    if res is None:
        return True
    elif 'affiliations_complete' not in res:
        return True
    elif res['affiliations_complete'] == []:
        return True
    return False

def fallback(soup, publisher=None):
    res = None
    try:
        print('fallback1')
        res = parse_sciendo(soup)
        if is_empty(res):
            print('fallback2')
            res = parse_generic(soup)
        if is_empty(res) and publisher == "Elsevier BV":
            res = parse_elsevier(soup)
    except:
        pass

    return res

def html_parser(doi, html, publisher=None):
    res = None
    
    if html in ['not_downloaded', 'error_ip_blocked', 'error', 'AVOID']:
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

    if html[0:4] == "%PDF":
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}

    if len(html) > 2000000 and ('<div' not in html):
        print("probably a pdf {}".format(doi))
        return {'is_french': None, 'authors_from_html':[], 'affiliations_complete':[], 'affiliations_fr':[]}
    
    soup = BeautifulSoup(html, 'lxml')

    if html == 'file too large':
        pass
    elif 'static.pubmed.gov' in html:
        res = parse_pubmed(soup)
    elif "<?xml version=\"1.0\" ?>\n<!DOCTYPE Pubmed" in html:
        res = parse_pubmed_api(soup)
    elif doi[0:7] == '10.1016':
        res = parse_elsevier(soup)
    elif doi[0:7] in ['10.1038']:
        res = parse_nature(soup)
    elif doi[0:7] in ['10.1007', '10.1140']:
        res = parse_springer(soup)
    elif doi[0:7] == '10.4000':
        res = parse_openedition(soup)
    elif doi[0:7] in ['10.1080', '10.1057', '10.4081']:
        res = parse_tandf(soup)
    elif doi[0:7] == '10.3917':
        res = parse_cairn(soup)
    elif doi[0:7] in ['10.1002', '10.1111']:
        res = parse_wiley(soup)
    elif doi[0:7] == '10.1051':
        res = parse_aanda(soup)
    elif doi[0:7] == '10.1021':
        res = parse_acs(soup)
    elif doi[0:7] == '10.1186':
        res = parse_bmc(soup)
    elif doi[0:7] == '10.1103':
        res = parse_aps(soup)
    elif doi[0:7] in ['10.1088', '10.3847']:
        res = parse_iop(soup)
    elif doi[0:7] == '10.3389':
        res = parse_frontiers(soup)
    elif doi[0:7] == '10.1039':
        res = parse_rsc(soup)
    elif doi[0:7] == '10.1371':
        res = parse_plos(soup)
    elif doi[0:7] == '10.1017':
        res = parse_cambridge(soup)
    elif doi[0:7] == '10.3390':
        res = parse_mdpi(soup)
    elif doi[0:7] == '10.1093':
        res = parse_oup(soup)
    elif doi[0:7] == '10.1063':
        res = parse_aip(soup)
    elif doi[0:7] == '10.1117':
        res = parse_spie(soup)
    elif doi[0:7] == '10.5194':
        res = parse_atmos_chem(soup)
    elif doi[0:7] == '10.1136':
        res = parse_bmj(soup)
    elif doi[0:7] == '10.1177':
        res = parse_sagepub(soup)
    elif doi[0:7] == '10.7202':
        res = parse_erudit(soup)
    elif doi[0:7] == '10.3233':
        res = parse_ios(soup)
    elif doi[0:7] in ['10.2139', '10.1364']:
        res = parse_ssrn(soup)
    elif doi[0:7] in ['10.1515', '10.1183', '10.1055', '10.1097', '10.1142', '10.1101', \
            '10.1158', '10.1121', '10.1115', '10.1108', '10.1089', '10.2174']:
        res = parse_sciendo(soup)
    elif doi[0:7] == '10.1155':
        res = parse_hindawi(soup)
    elif doi[0:7] in ['10.1109', '10.7873']:
        try:
            res = parse_ieee(soup)
        except:
            soup2 = BeautifulSoup(html, 'html.parser')
            res = parse_ieee(soup2)
    elif doi[0:7] == '10.1145':
        res = parse_acm(soup)
    
    if is_empty(res):
        res = fallback(soup, publisher)

    affiliations_complete = []
    if 'affiliations_complete' in res:
        for a in res['affiliations_complete']:
            if isinstance(a, str):
                affiliations_complete.append({'structure_name':a})
            elif isinstance(a,dict):
                affiliations_complete.append(a)
            else:
                print("error in parsing ! affiliations are not str or dict !")
    res['affiliations_complete'] = affiliations_complete

    if 'authors_from_html' in res:
        for a in res['authors_from_html']:
            a['role'] = 'author'

    return res
    
