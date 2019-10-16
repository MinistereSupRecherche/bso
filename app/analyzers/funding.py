"""Detection of country for authors affiliations."""
import requests
import json
import re
# from typing import Union, List, Dict, Any


def get_projects(funding_info):

    if funding_info is None or len(funding_info) == 0:
        return []

    anr_regex = re.compile("ANR-[0-9]{2}-[A-Z0-9]{4}-[0-9]{4}", re.IGNORECASE)
    pia_regex = re.compile("[0-9]{2}-[A-Z]{4}-[0-9]{4}", re.IGNORECASE)

    funding_ids = []
    for info in funding_info:
        if 'funding_ref' in info and len(info.get('funding_ref', '')) > 1:
            funding_ids.append(info['funding_ref'])

        for field in info:
            try:
                funding_ids += anr_regex.findall(info[field])
                funding_ids += pia_regex.findall(info[field])
            except Exception:
                pass

    funding_ids = [e.upper() for e in funding_ids]
    funding_ids = list(set(funding_ids))
    return funding_ids


def get_funding_from_hal(hal_id: str) -> str:
    url = "https://api.archives-ouvertes.fr/search/?q={}:{}"\
            .format('halId_s', hal_id)
    url += "&fl=europeanProjectAcronym_s,europeanProjectReference_s,"
    url += "europeanProjectTitle_s,anrProjectAcronym_s,"
    url += "anrProjectReference_s,anrProjectTitle_s,"
    url += "funding_s&rows=10&start=0"

    try:
        r = requests.get(url, timeout=2)
        result = json.loads(r.text)['response']['docs'][0]
        funding_info = []
        if 'funding_s' in result \
                and result['funding_s']:
            if isinstance(result['funding_s'], list):
                for elt in result['funding_s']:
                    funding_info.append({'funder': str(elt)})
            else:
                funding_info.append({
                    'funder': str(result['funding_s'])
                    })

        # European Project
        funding_info_elt = {'funder': 'European project'}

        if 'europeanProjectReference_s' in result \
                and result['europeanProjectReference_s']:
            funding_info_elt['funding_ref'] \
                      = str(result['europeanProjectReference_s'][0])

        if 'europeanProjectAcronym_s' in result \
                and result['europeanProjectAcronym_s']:
            funding_info_elt['project_acronym'] \
                    = str(result['europeanProjectAcronym_s'][0])

        if 'europeanProjectTitle_s' in result \
                and result['europeanProjectTitle_s']:
            funding_info_elt['project_title'] \
                    = str(result['europeanProjectTitle_s'][0])

        if len(funding_info_elt) > 1:
            funding_info.append(funding_info_elt)

        # ANR
        funding_info_elt = {'funder': 'ANR'}

        if 'anrProjectReference_s' in result \
                and result['anrProjectReference_s']:
            funding_info_elt['funding_ref'] \
                    = str(result['anrProjectReference_s'][0])

        if 'anrProjectAcronym_s' in result \
                and result['anrProjectAcronym_s']:
            funding_info_elt['project_acronym'] \
                    = str(result['anrProjectAcronym_s'][0])
        if 'anrProjectTitle_s' in result \
                and result['anrProjectTitle_s']:
            funding_info_elt['project_title'] \
                    = str(result['anrProjectTitle_s'][0])

        if len(funding_info_elt) > 1:
            funding_info.append(funding_info_elt)

        return funding_info
    except Exception:
        print("error in hal getting funding for id hal {}".format(hal_id))
        return None
