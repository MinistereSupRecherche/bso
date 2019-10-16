# from obj_utils import *
from dataesr_publication import get_publication_from_id_in_db
from publication_update import PublicationUpdate

from typing import Dict


class OpenAPCPublication():
    """
    """

    def __init__(self, **kwargs: Dict) -> None:
        super(OpenAPCPublication, self).__init__()
        self.result = []

        if 'doi' in kwargs:
            doi = kwargs['doi'].lower()
        else:
            self.status = 'error: no doi in argument'
            return

        publication_id = 'doi'+doi

        if 'euro' in kwargs:
            apc = kwargs['euro']

        if 'institution' in kwargs:
            institution_name = kwargs['institution']

        new_publication = {
            'id': publication_id,
            'apc': apc,
            'html_affiliations_info': [
                {'institution_name': institution_name}
            ]
        }
        existing_publication = get_publication_from_id_in_db(publication_id)
        if existing_publication is None:
            self.status = 'doi from open apc not in db ! {}'.format(doi)
        else:
            PublicationUpdate(q=None, **new_publication)
            self.status = 'ok'


if __name__ == '__main__':
    pass
