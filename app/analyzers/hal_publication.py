# import os
import json
import requests
import datetime
import re
from app.config import BaseConfig
from .requests_utils import requests_retry_session
from .obj_utils import add_object, normalize_doi
from .dataesr_publication import get_publication_from_id_in_db
from .dataesr_publication import get_publication_html_from_id_in_db
from .funding import get_funding_from_hal, get_projects
from .references_hal import get_references_from_hal
from .publication_update import PublicationUpdate
from typing import Any, Dict, Union
from app.utils.logger import create_logger
from .html_parsers.global_html_parser import html_parser

logger = create_logger(__name__)


class HALPublication():
    """
    """
    _URL = "https://api.archives-ouvertes.fr/search/?q={}:{}"
    _URL += "&fl=europeanProjectAcronym_s,europeanProjectReference_s,"
    _URL += "europeanProjectTitle_s,anrProjectAcronym_s,"
    _URL += "anrProjectReference_s,anrProjectTitle_s,"
    _URL += "authFullNameId_fs,authIdHasPrimaryStructure_fs,"
    _URL += "abstract_s,doiId_s,docid,modifiedDate_tdate,"
    _URL += "structIdName_fs,structCountry_s,halId_s,"
    _URL += "submittedDate_tdate,producedDate_tdate,en_keyword_s,"
    _URL += "fr_keyword_s,docType_s,title_s,journalEissn_s,journalIssn_s,"
    _URL += "journalPublisher_s,journalTitle_s,bookTitle_s,conferenceTitle_s,"
    _URL += "issue_s,openAccess_bool,page_s,licence_s,language_s,funding_s,"
    _URL += "domain_s,linkExtUrl_s,fileMain_s&rows=10000&start=0"

    _LOCAL_URL = BaseConfig.DATAESR_PUBLICATIONS_URL

    def replace_alpha(self, s):
        ans = ""
        for c in s:
            if c.isalpha():
                ans += '?'
            else:
                ans += c
        return ans

    def __init__(self, **kwargs: Dict) -> None:
        super(HALPublication, self).__init__()
        doi, id_hal_publi = None, None
        if 'id_hal' in kwargs:
            id_hal_publi = kwargs['id_hal']
            logger.info("id_hal in kwargs: {}".format(id_hal_publi))
        if 'doi' in kwargs:
            doi = normalize_doi(kwargs['doi'])
            logger.info("doi in kwargs: {}".format(doi))
        if doi is None and id_hal_publi is None:
            self.result = []
            self.status = 'error: nor doi neither id_hal in argument'
            return
        if id_hal_publi:
            self.url = self._URL.format('halId_s', id_hal_publi)
        elif doi:
            self.url = self._URL.format('doiId_id', doi)
        self.error = False
        self.result = self._get_response()

        #if 'doi' in kwargs:
        #    # we keep only the right DOIs
        #    results_filtered = []
        #    for res in self.result:
        #        if 'doiId_s' in res and \
        #                normalize_doi(res['doiId_s']) == doi.lower():
        #            results_filtered.append(res)

        #    self.result = results_filtered

        num_found = len(self.result)
        if num_found == 1:
            self.status = 'one_found'
        elif num_found > 1:
            self.status = 'multiple_found'
        elif num_found == 0:
            self.status = 'not_found'

        if self.status in ['one_found', 'multiple_found']:
            new_publication = {'data_sources': ['HAL']}
            result = self.result[0]

            if 'halId_s' not in result:
                self.status = 'not_found'
                return

            if 'doiId_s' in result and result['doiId_s']:
                doi = normalize_doi(result['doiId_s'])
            if doi is not None:
                logger.info("doi {}".format(doi))
                if 'doiId_s' not in result:
                    logger.info("adding doi {} for id_hal {}".format(doi, result['halId_s']))

                publication_id = 'doi'+doi
                new_publication['id'] = publication_id
                new_publication['doi'] = doi

                if ('/' not in new_publication['doi']) \
                        or (len(new_publication['doi']) < 8) \
                        or ('???' in new_publication['doi']) \
                        or (' ' in new_publication['doi']) \
                        or ('xxxx' in new_publication['doi']):
                    logger.info(
                            "wrong doi from HAL : {}".format(
                                new_publication['doi']))
                    return

            if 'halId_s' in result:
                id_hal_publi = result['halId_s'].lower()
                new_publication['id_hal'] = result['halId_s'].lower()
                new_publication['funding_info'] = \
                    get_funding_from_hal(result['halId_s'].lower())
                new_publication['projects'] = get_projects(new_publication['funding_info'])
                new_publication['id_references'] = \
                    get_references_from_hal(result['halId_s'])

            if 'structCountry_s' in result \
                    and 'fr' in result['structCountry_s']:
                new_publication['is_french'] = True
            else:
                new_publication['is_french'] = False

            if 'abstract_s' in result:
                new_publication['summary'] = " ".join(result['abstract_s'])

            if 'domain_s' in result:
                new_publication['thematics'] = []
                for d in result['domain_s']:
                    current_domain = {'code': d, 'reference': 'HAL'}
                    labels = get_domain(".".join(d.split('.')[1:]))
                    if 'fr_label' in labels and labels['fr_label']:
                        current_domain['fr_label'] = labels['fr_label']
                    if 'en_label' in labels and labels['en_label']:
                        current_domain['en_label'] = labels['en_label']

                    new_publication['thematics'].append(current_domain)

            macro_level = get_macro_level_barometre(new_publication)
            if macro_level:
                has_macro_level = False
                for t in new_publication.get('thematics', []):
                    if t.get('reference') == 'macro_level_barometre':
                        t['en_label'] = macro_level['en_label']
                        t['fr_label'] = macro_level['fr_label']
                        has_macro_level = True

                if has_macro_level is False:
                    new_publication['thematics'].append(macro_level)

            new_publication['is_oa'] = False

            # set a boolean for future identification
            new_publication['persons_identified'] = False
            new_publication['structures_identified'] = False

            if 'openAccess_bool' in result and result['openAccess_bool']:
                new_publication['is_oa'] = result['openAccess_bool']

            if new_publication['is_oa']:
                new_publication['oa_evidence'] = {}

            if 'fileMain_s' in result and new_publication['is_oa']:
                new_publication['oa_evidence']['url'] = result['fileMain_s']

            if 'linkExtUrl_s' in result and new_publication['is_oa'] \
                    and 'url' not in new_publication['oa_evidence']:
                new_publication['oa_evidence']['url'] = result['linkExtUrl_s']

            repository_regex = re.compile(
                    r"(hal|arxiv|archives-ouvertes|europepmc)(\.|-)")
            journal_rgx = "(academic.oup.com)|(hindawi.com)|(wiley.com)"
            journal_rgx += "|(springer.com)|(openedition)|(asm.org)"
            journal_rgx += "|(mdpi.com)"
            journal_regex = re.compile(journal_rgx)

            if 'oa_evidence' in new_publication \
                    and 'url' in new_publication['oa_evidence']:
                        url = new_publication['oa_evidence']['url'].lower()

                        if re.search(repository_regex, url):
                            new_publication['oa_evidence']['host_type'] \
                                    = 'repository'

                        if re.search(journal_regex, url):
                            new_publication['oa_evidence']['host_type'] \
                                    = 'publisher'

            if 'licence_s' in result and new_publication['is_oa']:
                new_publication['oa_evidence']['license'] = result['licence_s']

            if 'producedDate_tdate' in result:
                new_publication['publication_date'] = \
                        datetime.datetime.strptime(
                        result["producedDate_tdate"][0:10], '%Y-%m-%d'
                        ).isoformat()

            if 'modifiedDate_tdate' in result and new_publication['is_oa']:
                parsed_date = datetime.datetime.strptime(
                        result["modifiedDate_tdate"][0:10], '%Y-%m-%d'
                ).isoformat()
                new_publication['first_time_seen_oa_date'] = \
                    parsed_date
                new_publication['oa_locations_history'] = [new_publication['oa_evidence'].copy()]
                new_publication['oa_locations_history'][0]['updated'] = parsed_date
                new_publication['oa_locations_history'][0]['is_oa'] = True
                new_publication['oa_locations'] = new_publication['oa_locations_history']

            if 'en_keyword_s' in result and result['en_keyword_s']:
                new_publication['keywords_en'] = result['en_keyword_s']

            if 'fr_keyword_s' in result and result['fr_keyword_s']:
                new_publication['keywords_fr'] = result['fr_keyword_s']

            new_publication['genre'] = "other"
            if 'docType_s' in result and result['docType_s']:
                new_publication['genre'] = result['docType_s']
                if new_publication['genre'] == 'ART':
                    new_publication['genre'] = 'journal-article'
                elif new_publication['genre'] == 'COMM':
                    new_publication['genre'] = 'proceedings-article'
                elif new_publication['genre'] in ['DOUV', 'OUV']:
                    new_publication['genre'] = 'book'
                elif new_publication['genre'] in ['COUV']:
                    new_publication['genre'] = 'book-chapter'
                elif new_publication['genre'] in ['UNDEFINED']:
                    new_publication['genre'] = 'other'
                else:
                    new_publication['genre'] = new_publication['genre'].lower()

            if 'title_s' in result and result['title_s']:
                new_publication['title'] = ";".join(result['title_s'])

            if 'language_s' in result and result['language_s']:
                new_publication['language'] = ";".join(result['language_s'])

            new_publication['source'] = {}
            if 'journalTitle_s' in result and result['journalTitle_s']:
                new_publication['source']['source_title'] \
                        = result['journalTitle_s']
            elif 'bookTitle_s' in result and result['bookTitle_s']:
                new_publication['source']['source_title'] \
                        = result['bookTitle_s']
            elif 'conferenceTitle_s' in result and result['conferenceTitle_s']:
                new_publication['source']['source_title'] \
                        = result['conferenceTitle_s']

            if 'journalPublisher_s' in result and result['journalPublisher_s']:
                new_publication['source']['publisher'] \
                        = result['journalPublisher_s']
            if 'issue_s' in result and result['issue_s']:
                new_publication['source']['issue'] \
                        = ";".join(result['issue_s'])

            if 'journalIssn_s' in result \
                    or 'journalEissn_s' in result:
                new_publication['source']['journal_issns'] = []

            issn_regex = re.compile("(....)-(....)")
            if 'journalIssn_s' in result:
                if re.search(issn_regex, result['journalIssn_s']):
                    new_publication['source']['journal_issns']\
                        .append(result['journalIssn_s'])
            if 'journalEissn_s' in result:
                if re.search(issn_regex, result['journalEissn_s']):
                    new_publication['source']['journal_issns']\
                        .append(result['journalEissn_s'])

            if 'page_s' in result and result['page_s']:
                new_publication['source']['pagination'] = result['page_s']

            new_publication['id_external'] = []
            for id_external in [
                    'halId_s', 'docid']:
                if id_external in result:
                    new_publication['id_external'] = \
                            add_object(
                                new_publication['id_external'],
                                {
                                    'id_type': id_external,
                                    'id_value': str(result[id_external])
                                }
                            )

            persons_map = {}
            new_publication['hal_authors_info'] = []
            if 'authIdHasPrimaryStructure_fs' in result:
                nb_aut = len(result['authIdHasPrimaryStructure_fs'])

                new_publication['hal_authors_info'] \
                    = result['authIdHasPrimaryStructure_fs']
                new_publication['authors'] = []
                for person in result['authIdHasPrimaryStructure_fs']:
                    sp = person.split('_JoinSep_')
                    author_doc_id = sp[0].split('_FacetSep_')[0]
                    full_name = sp[0].split('_FacetSep_')[1]

                    id_hal, last_name, first_name = None, None, None
                    if (nb_aut <= 10):
                        author_infos = get_author_info_from_hal(author_doc_id)
                        id_hal = author_infos['id_hal']
                        last_name = author_infos['last_name']
                        first_name = author_infos['first_name']
                    else:
                        logger.debug(
                                "too much authIdHasPrimary - keep fullname")

                    struct_doc_id, struct_fullname = (
                            sp[1].split('_FacetSep_')[0],
                            sp[1].split('_FacetSep_')[1]
                    )
                    current_affiliation_str = struct_fullname
                    current_affiliation_str += ' ; docid_hal_'+struct_doc_id
                    current_affiliation_info = {
                        'structure_name': current_affiliation_str
                    }

                    if author_doc_id not in persons_map:
                        persons_map[author_doc_id] = {
                            'full_name': full_name,
                            'docid_hal': author_doc_id,
                            'role': 'author',
                            'affiliations_info': [current_affiliation_info]
                        }
                        if id_hal:
                            persons_map[author_doc_id]['id_hal'] = id_hal
                        if last_name:
                            persons_map[author_doc_id]['last_name'] = last_name
                        if first_name:
                            persons_map[author_doc_id]['first_name'] = first_name
                    else:
                        persons_map[author_doc_id]['affiliations_info']\
                                .append(current_affiliation_info)

            if 'authFullNameId_fs' in result:
                nb_aut = len(result['authFullNameId_fs'])
                logger.info("{} elts in authFullNameId".format(nb_aut))
                for person in result['authFullNameId_fs']:
                    author_doc_id = person.split('_FacetSep_')[1]
                    author_fullname = person.split('_FacetSep_')[0]
                    if author_doc_id not in persons_map:
                        new_publication['hal_authors_info'].append(
                                author_doc_id+'_FacetSep_'+author_fullname
                                )
                        id_hal, first_name, last_name = None, None, None
                        if (nb_aut <= 10):
                            author_infos = get_author_info_from_hal(author_doc_id)
                            id_hal = author_infos['id_hal']
                            last_name = author_infos['last_name']
                            first_name = author_infos['first_name']
                        else:
                            logger.debug(
                                    "too much authIdHasPrimaryS ->full name")

                        persons_map[author_doc_id] = {
                            'full_name': author_fullname,
                            'docid_hal': author_doc_id,
                            'role': 'author'
                        }
                        if id_hal:
                            persons_map[author_doc_id]['id_hal'] = id_hal
                        if last_name:
                            persons_map[author_doc_id]['last_name'] = last_name
                        if first_name:
                            persons_map[author_doc_id]['first_name'] = first_name

            new_publication['authors'] = [
                persons_map[e] for e in persons_map
            ]

            html_obj = get_publication_html_from_id_in_db(publication_id)

            html = None
            if html_obj:
                html = html_obj.get('notice')
            if html:
                logger.info(
                        "HAL starting html parser for {}".format(
                            new_publication['doi']))
                parsed_info = html_parser(new_publication['doi'], html)

                if 'authors_from_html' in parsed_info:
                    authors_from_html = parsed_info['authors_from_html']
                    new_publication['html_authors_info'] = authors_from_html

                if 'is_french' in parsed_info and (
                        parsed_info['is_french'] is True
                        ):
                    new_publication['is_french'] = parsed_info['is_french']
                if 'affiliations_complete' in parsed_info:
                    new_publication['html_affiliations_info'] \
                            = parsed_info['affiliations_complete']

                if 'keywords' in parsed_info \
                        and parsed_info['keywords'] \
                        and len(parsed_info['keywords']) > 0:
                    if 'keywords_en' not in new_publication:
                        new_publication['keywords_en'] = []
                    new_publication['keywords_en'] += parsed_info['keywords']

            existing_publication = \
                get_publication_from_id_in_db(publication_id)
            if existing_publication is None:
                r = requests.post(self._LOCAL_URL, json=[new_publication])
                if r.ok is False:
                    logger.debug(
                            "Error in inserting publi {}".format(
                                publication_id))
                    logger.debug(r.text)
                    logger.debug(new_publication)

                logger.info("start update 1")
                PublicationUpdate(q=None, **new_publication)
                logger.info("end update 1")
            else:
                for field in ['publication_date', 'source', 'oa_locations', 'oa_locations_history']:
                    if field in existing_publication \
                            and field in new_publication:
                        del new_publication[field]
                        logger.info(
                                "deleting field {}".format(field))

                if 'genre' in existing_publication \
                        and 'genre' in new_publication \
                        and existing_publication['genre'].upper() != existing_publication['genre']:
                            del new_publication['genre']

                logger.info(new_publication)
                PublicationUpdate(q=None, **new_publication)

    def _get_response(self) -> Any:
        """ - Query self.url
        """
        try:
            r = requests_retry_session().get(self.url)
            if r.status_code == 200:
                json_response = r.json()
                if json_response:
                    response = json_response.get('response')
                    if response:
                        response = response.get('docs')
            else:
                response = []

            if response is None:
                return []

        except requests.exceptions.RequestException as err:
            self.error = u'ERROR - {}'.format(str(err))  # type:ignore
            return []

        return response


def get_author_info_from_hal(docid) -> Dict:
    idHal, last_name, first_name = None, None, None
    url = BaseConfig.HAL_URL_AUTHOR
    r = requests_retry_session()\
        .get(
            url+"?q=docid:%22{}%22&fl=*".format(docid)
            )
    if r.ok:
        try:
            response = json.loads(r.text).get('response')
            if response:
                docs = response.get('docs')
                if docs and len(docs) == 1:
                    idHal = docs[0].get("idHal_i")
                    last_name = docs[0].get("lastName_s")
                    first_name = docs[0].get("firstName_s")
        except Exception:
            pass

    if idHal == 0:
        idHal = None
    else:
        idHal = str(idHal)

    return {'id_hal': idHal, 'last_name': last_name, 'first_name': first_name}


def get_domain(code: str) -> Dict:
    en_domain, fr_domain = None, None
    url = BaseConfig.HAL_URL_DOMAIN

    r = requests_retry_session()\
        .get(url + "?q=code_s:%22{}%22&fl=*_domain_s,code_s".format(code))
    if r.ok:
        try:
            response = json.loads(r.text).get('response')
            if response:
                docs = response.get('docs')
                if docs and len(docs) == 1:
                    en_domain = docs[0].get("en_domain_s")
                    fr_domain = docs[0].get("fr_domain_s")
        except Exception:
            pass

    return {'en_label': en_domain, 'fr_label': fr_domain}

def get_macro_level_barometre(new_publication):
    res = {'reference': 'macro_level_barometre'}
    for t in new_publication.get('thematics', []):
        if 'HAL' == t.get("reference"):
            if t.get("code") == "chim" or "chim." in t.get("code"):
                res['en_label'] = "Chemistry"
                res['fr_label'] = "Chimie"
                return res
            if t.get("code") == "math" or "math." in t.get("code") or t.get("code") == "stat" or "stat." in t.get("code"):
                res['en_label'] = "Mathematics"
                res['fr_label'] = "Mathématiques"
                return res
            if t.get("code") == "info" or "info." in t.get("code"):
                res['en_label'] = "Computer and \n information sciences"
                res['fr_label'] = "Informatique et sciences de l'information"
                return res
            if t.get("code") == "nlin" or "nlin." in t.get("code") \
                    or "astro-ph" in t.get("code") or "cond-mat" in t.get("code") \
                    or "hep-" in t.get("code") or 'nucl-' in t.get("code"):
                res['en_label'] = "Physical sciences, Astronomy"
                res['fr_label'] = "Sciences physiques, Astronomie"
                return res
    return None


if __name__ == '__main__':
    pass
