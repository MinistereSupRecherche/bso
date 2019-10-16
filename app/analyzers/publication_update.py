# import os
import requests
import copy
from app.config import BaseConfig
from .dataesr_publication import get_publication_from_id_in_db
from .obj_utils import update_elt, normalize_doi
from app.utils.strings import normalize_name
# from .country_detection import get_country_from_hal
from app.utils.logger import create_logger
from typing import Dict


logger = create_logger(__name__)


class PublicationUpdate():
    """
    """
    _URL = BaseConfig.DATAESR_PUBLICATIONS_URL
    _TIMEOUT = 5.0

    def __init__(self, q: str, **kwargs: Dict) -> None:
        super(PublicationUpdate, self).__init__()

        self._update(**kwargs)

    def _update(self, **kwargs: Dict) -> None:
        publication_id = normalize_doi(kwargs.get('id'))
        if publication_id is None:
            logger.info("no publication id specified in update!")
            return

        has_changed = False

        if 'authors' in kwargs and kwargs['authors']:
            clean_authors(kwargs['authors'])
        if 'html_authors_info' in kwargs and kwargs['html_authors_info']:
            clean_authors(kwargs['html_authors_info'])

        existing_publication = get_publication_from_id_in_db(publication_id)
        if existing_publication is None:
            logger.info("No publication id {} in database !!".format(publication_id))
            return

        etag = existing_publication['etag']

        existing_publication = clean_object(existing_publication)
        del existing_publication['id']

        kwargs = clean_object(kwargs)
        new_publication = copy.deepcopy(existing_publication)

        if 'first_time_seen_oa_date' in existing_publication \
                and 'first_time_seen_oa_date' in kwargs:
                    new_publication['first_time_seen_oa_date'] = min(
                        existing_publication['first_time_seen_oa_date'],
                        kwargs['first_time_seen_oa_date'])
                    # cannot be before publication date !
                    new_publication['first_time_seen_oa_date'] = max(
                        new_publication['first_time_seen_oa_date'],
                        new_publication['publication_date'])

                    del kwargs['first_time_seen_oa_date']

        for field in ['authors', 'html_authors_info', 'hal_authors_info', 'html_affiliations_info']:
            if field in kwargs and field in existing_publication and isinstance(kwargs[field], list) and \
                    len(kwargs[field]) > 10:
                        logger.info("remove field {} from update".format(field))
                        del kwargs[field]


        info_to_update = kwargs

        if 'oa_locations_history' in new_publication and \
                'oa_locations_history' in kwargs:
            new_publication['oa_locations_history'] = \
                    kwargs['oa_locations_history']

        if new_publication.get('persons_identified') and 'persons_identified' in kwargs:
            del kwargs['persons_identified']
        if new_publication.get('structures_identified') and 'structures_identified' in kwargs:
            del kwargs['structures_identified']

        # id_hal_publi = None
        if 'id_external' in new_publication:
            for elt in new_publication['id_external']:
                if 'id_type' in elt and elt['id_type'] == 'halId_s':
                    new_publication['id_hal'] = elt['id_value']
                    # id_hal_publi = new_publication['id_hal']

        logger.debug("starting updating elts")
        logger.debug(info_to_update.keys())
        new_publication = update_elt(new_publication, info_to_update)
        logger.debug("done")

        add_html_authors = False
        if 'html_authors_info' in new_publication \
                and 'authors' in new_publication:
                    for a in new_publication['html_authors_info']:
                        if 'affiliations_info' in a and a['affiliations_info']:
                            add_html_authors = True
                            break
        if add_html_authors:
            new_publication['authors'] += new_publication['html_authors_info']

        # merging all persons
        logger.info("{} authors to merge in publication update".format(len(new_publication['authors'])))
        persons_map = {}
        short_to_long = {}

        # a first round to get the correspondance short -> long keys
        for person in new_publication['authors']:
            key = ""
            if 'last_name' in person and person['last_name']:
                key_tmp = sort_words(person['last_name'])
                if 'first_name' in person and person['first_name']:
                    key_tmp += " " + sort_words(person.get('first_name', ''))
                key = sort_words(key_tmp, False)

                key_short_tmp = sort_words(person['last_name'])
                if 'first_name' in person and person['first_name']:
                    key_short_tmp += " " + \
                            sort_words(person['first_name'][0:1])
                key_short = sort_words(key_short_tmp, False)

                if len(key) > len(key_short):
                        short_to_long[key_short] = key

        for person in new_publication['authors']:
            key = ""
            if 'last_name' in person and person['last_name']:
                key_tmp = sort_words(person['last_name'])
                if 'first_name' in person and person['first_name']:
                    key_tmp += " " + sort_words(person['first_name'])
                key = sort_words(key_tmp, False)
                if key in short_to_long:
                    key = short_to_long[key]
            elif 'full_name' in person and person['full_name']:
                key_full = sort_words(person['full_name'], False)
                if key_full in short_to_long:
                    key = short_to_long[key_full]
                else:
                    key = key_full

            if key == "":
                continue

            if key not in persons_map:
                persons_map[key] = []
            persons_map[key].append(person)

        new_authors = []
        for k in persons_map:
            new_author = merge_authors(persons_map[k])
            new_authors.append(new_author)
        
        for person in new_authors:
            if person.get('full_name','') == '':
                full_name = person.get('last_name', '') + ' ' + person.get('first_name', '')
                person['full_name'] = full_name.strip()

        new_publication['authors'] = new_authors
        logger.info("{} authors after merge".format(len(new_publication['authors'])))

        if new_publication.get('is_oa'):
            host_types = []
            for oa_loc in new_publication.get('oa_locations', []):
                if 'host_type' in oa_loc and oa_loc['host_type']:
                    host_types.append(oa_loc['host_type'])
            host_types = list(set(host_types))
            host_types.sort()
            if new_publication.get('is_oa') and len(host_types) == 0:
                host_types = ['unknown']
            new_publication['oa_host_type'] = ";".join(host_types)
        else:
            new_publication['oa_host_type'] = "closed"

        # if 'fields_only' not in new_publication:
        #    if id_hal_publi:
        #        funding_info = get_funding_from_hal(id_hal_publi)
        #        if funding_info:
        #            new_publication['funding_info'] = \
        #                    get_funding_from_hal(id_hal_publi)
        #        elif 'funding_info' in new_publication:
        #            del new_publication['funding_info']
        #    elif 'funding_info' in new_publication:
        #        new_funding_list = []
        #        for funding_elt in new_publication['funding_info']:
        #            if isinstance(funding_elt, str):
        #                new_funding_list.append({'funder': funding_elt})
        #        new_publication['funding_info'] = new_funding_list

        has_changed = True

        # if 'fields_only' not in new_publication \
        #        and 'check_country_hal' in kwargs \
        #        and kwargs['check_country_hal']:
        #    if 'hal_authors_info' in new_publication \
        #            and new_publication['hal_authors_info']:
        #        for person in new_publication['hal_authors_info']:
        #            sp = person.split('_JoinSep_')
        #            if len(sp) > 0:
        #                struct_doc_id, struct_fullname = (
        #                        sp[1].split('_FacetSep_')[0],
        #                        sp[1].split('_FacetSep_')[1]
        #                )
        #                if get_country_from_hal(struct_doc_id) == 'France':
        #                    new_publication['is_french'] = True
        #                    break

        if 'id' in new_publication:
            del new_publication['id']

        self.status = 'nothing done'
        if has_changed:
            url = self._URL + '/' + publication_id
            headers = {'If-Match': etag}

            r = requests.patch(url, headers=headers, json=new_publication)
            if r.ok is False:
                logger.error(new_publication)
                logger.error("update went wrong for {}".format(publication_id))
                logger.error(r.text)
                self.status = 'KO'
            else:
                self.status = 'OK'


def clean_object(obj):
    for field in ['modified_at', 'created_at', '_id', 'etag', 'hrefs']:
        if field in obj:
            del obj[field]

    for e in obj:
        if isinstance(obj[e], list) \
                and len(obj[e]) > 0 \
                and isinstance(obj[e][0], dict) \
                and 'meta' in obj[e][0]:
            for elt in obj[e]:
                del elt['meta']
    return obj


def clean_authors(obj):
    for author in obj:
        if 'data_source' in author:
            del author['data_source']

        if 'affiliations_info' in author and author['affiliations_info']:
            for k in author['affiliations_info']:
                if 'start_date' in k:
                    del k['start_date']


def sort_words(x, remove_unit_word=True):
    v = normalize_name(x).split(" ")
    v_minus_init = [e for e in v if len(e) > 1]
    if remove_unit_word and len(v_minus_init) > 0:
        v = v_minus_init
    v.sort()
    return " ".join(v)


def merge_authors(authors):
    res = {}
    for a in authors:
        for field in a:

            if field in ["affiliations_info", "affiliations"]:
                if field not in res:
                    res[field] = []
                for aff in a[field]:
                    if 'meta' in aff:
                        del aff['meta']
                    if aff and aff not in res[field]:
                        res[field].append(aff)

            elif a[field] is not None:
                res[field] = a[field]
    return(res)


if __name__ == '__main__':
    pass
