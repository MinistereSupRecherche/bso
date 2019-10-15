# import os
import requests
import datetime
import re
from bs4 import BeautifulSoup
from app.config import BaseConfig
# from obj_utils import *
from .dataesr_publication import get_publication_html_from_id_in_db
from .dataesr_publication import get_publication_from_id_in_db
from .obj_utils import normalize_doi
from .publication_update import PublicationUpdate
from .hal_publication import HALPublication
from .html_parsers.global_html_parser import html_parser
from .html_parsers.doi_utils import fr_regex
from app.utils.logger import create_logger
from typing import Dict

logger = create_logger(__name__)


def filter_oa_loc_field(oa_locations):
    oa_loc_field = ["host_type", "is_oa", "is_best", "version", "updated",
                    "url", "url_for_pdf", "url_for_landing_page", "pmh_id",
                    "evidence", "endpoint_id",
                    "repository_institution", "license"]
    res = []
    for oa_loc in oa_locations:
        new_elt = {}
        for f in oa_loc_field:
            if f in oa_loc:
                new_val = oa_loc[f]
                # update date should start with a 2 (eg 2018)
                if f == "updated" and new_val[0:1] != '2':
                    new_val = None
                if new_val is not None:
                    new_elt[f] = new_val
        if new_elt not in res:
            res.append(new_elt)
    return res


class UnpaywallPublication():
    """
    """
    _URL = BaseConfig.DATAESR_NOTICES_PUBLICATIONS_URL
    _LOCAL_URL = BaseConfig.DATAESR_PUBLICATIONS_URL

    def __init__(self, **kwargs: Dict) -> None:
        super(UnpaywallPublication, self).__init__()
        self.verbose = kwargs.get('verbose', False)

        if 'doi' in kwargs and kwargs['doi']:
            doi = normalize_doi(kwargs['doi'])
            publication_id = 'doi'+doi.lower()
        else:
            self.result = []
            self.status = 'error: no doi in argument'
            return

        publisher = None
        if 'publisher' in kwargs and kwargs['publisher']:
            publisher = kwargs['publisher']

        self.error = False
        new_publication = {'data_sources': ['Unpaywall']}

        # publication_year = None
        if 'published_date' in kwargs:
            parsed_date = datetime.datetime.strptime(
                kwargs['published_date'], "%Y-%m-%d"
            )
            new_publication['publication_date'] = parsed_date.isoformat()
            # publication_year = parsed_date.year

        new_publication['id'] = publication_id
        new_publication['doi'] = doi
        new_publication['is_french'] = False

        authors = []
        has_affiliations_info = False
        if 'z_authors' in kwargs and kwargs['z_authors']:
            for a in kwargs['z_authors']:
                if a is None:
                    continue

                author = {}
                if 'given' in a and a['given']:
                    author['first_name'] = a['given']
                if 'family' in a and a['family']:
                    author['last_name'] = a['family']
                if 'affiliation' in a and a['affiliation']:
                    has_affiliations_info = True
                    author['affiliations_info'] = []
                    for elt in a['affiliation']:
                        structure_name = ""
                        for f in elt:
                            structure_name += elt[f]+" "
                        author['affiliations_info'].append(
                            {'structure_name': structure_name}
                            )
                        if re.search(fr_regex, structure_name.lower()):
                            new_publication['is_french'] = True
                author['role'] = 'author'
                authors.append(author)

        new_publication['authors'] = authors
        logger.debug("{} authors in publi".format(len(authors)))

        existing_publication = get_publication_from_id_in_db(publication_id)
        # do not get html if publi already exists,
        # the work has already been done once
        # except force_parsing is passed in kwargs
        if 'avoid_parsing' in kwargs:
            html_obj = None
        elif existing_publication is None or 'force_parsing' in kwargs:
            html_obj = get_publication_html_from_id_in_db(publication_id)
        elif existing_publication and existing_publication.get('is_french', False) is True:
            html_obj = get_publication_html_from_id_in_db(publication_id)
        else:
            logger.info("not parsing html for doi {}".format(doi))
            html_obj = None

        html = None
        if html_obj:
            html = html_obj.get('notice')

        parse_html = False
        if html:
            if "<?xml version=\"1.0\" ?>\n<!DOCTYPE Pubmed" in html:
                parse_html = True
            elif has_affiliations_info:
                parse_html = False
            else:
                parse_html = True

        if parse_html:
            parsed_info = html_parser(doi, html, publisher)

            if 'authors_from_html' in parsed_info:
                authors_from_html = parsed_info['authors_from_html']

                # for author in authors_from_html:
                #    if 'affiliations_info' in author:
                #        for elt in author['affiliations_info']:
                #            elt['year'] = publication_year

                new_publication['html_authors_info'] = authors_from_html

            if 'is_french' in parsed_info and (
                    parsed_info['is_french'] is not None
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

            if 'id_external' in parsed_info:
                if 'id_external' not in new_publication:
                    new_publication['id_external'] = []
                new_publication['id_external'] += parsed_info['id_external']

        # beware : the boolean is_oa is put only if true !
        new_publication["genre"] = "other"
        for field in ["genre", "is_oa"]:
            if field in kwargs and kwargs[field]:
                new_publication[field] = kwargs[field]

        # this is necessary to parse title as sometimes,
        # there is some html in it!
        if 'title' in kwargs and kwargs['title']:
            new_publication['title'] = \
                    BeautifulSoup(kwargs['title'], 'lxml').get_text()

        # set a boolean for future identification
        new_publication['persons_identified'] = False
        new_publication['structures_identified'] = False

        new_publication['source'] = {}
        if 'publisher' in kwargs and kwargs['publisher']:
            new_publication['source']['publisher'] = kwargs['publisher']

        if 'journal_issns' in kwargs and kwargs['journal_issns']:
            new_publication['source']['journal_issns']\
                    = kwargs['journal_issns'].split(',')

        if 'journal_name' in kwargs and kwargs['journal_name']:
            new_publication['source']['source_title'] = kwargs['journal_name']

        if 'journal_is_oa' in kwargs and kwargs['journal_is_oa']:
            new_publication['source']['source_is_oa'] = kwargs['journal_is_oa']

        if 'journal_is_in_doaj' in kwargs and kwargs['journal_is_in_doaj']:
            new_publication['source']['source_is_in_doaj']\
                    = kwargs['journal_is_in_doaj']

        if 'updated' in kwargs and kwargs['updated']:
            new_publication['updated'] = kwargs['updated'].split('.')[0]

        if 'best_oa_location' in kwargs and kwargs['best_oa_location']:
            new_publication['oa_evidence'] = {}
            for field in [
                'host_type', 'version', 'license',
                'url', 'url_for_pdf', 'url_for_landing_page'
            ]:
                if field in kwargs['best_oa_location'] \
                        and kwargs['best_oa_location'][field]:
                    new_publication['oa_evidence'][field]\
                            = kwargs['best_oa_location'][field]
            if 'updated' in kwargs['best_oa_location'] \
                    and kwargs['best_oa_location']['updated']:
                date_str = kwargs['best_oa_location']['updated']
                parsed_date = date_str.split('.')[0]
                new_publication['first_time_seen_oa_date'] = \
                    parsed_date

        if 'oa_locations' in kwargs and kwargs['oa_locations']:
            new_publication['oa_locations'] = \
                    filter_oa_loc_field(kwargs['oa_locations'])
            for oa_loc in new_publication['oa_locations']:
                if 'updated' in oa_loc and oa_loc['updated']:
                    date_str = oa_loc['updated']
                    oa_loc['updated'] = date_str.split('.')[0]

        if 'oa_locations_history' in kwargs and kwargs['oa_locations_history']:
            new_publication['oa_locations_history'] = \
                    filter_oa_loc_field(kwargs['oa_locations_history'])

            for oa_loc in new_publication['oa_locations_history']:
                if 'updated' in oa_loc and oa_loc['updated'] is not None:
                    date_str = oa_loc['updated']
                    parsed_date = date_str.split('.')[0]
                    oa_loc['updated'] = date_str.split('.')[0]

                    if 'is_oa' in oa_loc and oa_loc['is_oa']:
                        if "first_time_seen_oa_date" not in new_publication:
                            new_publication['first_time_seen_oa_date'] = \
                                parsed_date
                        else:
                            new_publication['first_time_seen_oa_date'] = \
                                    min(new_publication[
                                        'first_time_seen_oa_date'],
                                        parsed_date)

        self.result = [new_publication]
        if existing_publication is None:
            r = requests.post(self._LOCAL_URL, json=[new_publication])
            if r.ok is False:
                logger.debug(
                        "Error in inserting publi {}".format(publication_id))
                logger.debug(r.text)
            PublicationUpdate(q=None, **new_publication)
        else:
            # if existing publi flagged as french, keep it
            if 'is_french' in existing_publication \
                    and existing_publication['is_french']:
                new_publication['is_french'] = True

            for oa_loc in existing_publication.get('oa_locations', []):
                if "https://hal.archives-ouvertes.fr/hal-" in \
                        oa_loc.get('url', ""):
                    if 'id_hal' not in existing_publication \
                            or existing_publication['id_hal'] is None:
                        id_hal = oa_loc['url']\
                                .replace(
                                        "https://hal.archives-ouvertes.fr/",
                                        "")\
                                .split('/')[0]
                        logger.info(
                                "setting HAL publi {} for unpaywall notice {}"
                                .format(id_hal, doi))
                        HALPublication(
                                q=None,
                                **{'doi': new_publication['doi'],
                                    'id_hal': id_hal})

            logger.debug("updating publi {}".format(publication_id))
            PublicationUpdate(q=None, **new_publication)

        self.status = 'ok'


if __name__ == '__main__':
    pass
