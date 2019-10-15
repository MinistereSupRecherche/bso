# import os
from app.config import BaseConfig
# from flask import current_app as app
import requests
from typing import Any, Dict, Union


class DataESRPublication():
    """
    """

    _URL = BaseConfig.DATAESR_PUBLICATIONS_URL
    _URL_HTML = BaseConfig.DATAESR_NOTICES_PUBLICATIONS_URL
    _TIMEOUT = 5.0

    def __init__(self, q: str, **kwargs: Dict) -> None:
        super(DataESRPublication, self).__init__()
        doi = kwargs.get('doi')
        self.query = q
        self.error = False
        self.status: Union[None, str] = None
        self.url = self._build_url_exact(q, **kwargs)
        self.result = self._get_response()
        self.status = 'not_found'

        self.match = []
        if self.result is None:
            print("ERROR DataESRPublication for {}".format(doi))
            return

        num_found = len(self.result)
        self.match = kwargs

        if num_found == 1:
            self.status = 'one_found'

        elif num_found > 1:
            self.status = 'multiple_found'
        elif num_found == 0:
            self.status = 'not_found'

        if 'one_found' in self.status:
            self.match = kwargs
            self.match['id'] = self.result[0]['id']

    def _get_response(self) -> Any:
        """ - Query self.url
        """
        try:
            r = requests.get(self.url)
            if r.status_code == 200:
                response = r.json()['data']
            else:
                response = []

        except requests.exceptions.RequestException as err:
            self.error = u'ERROR - {}'.format(str(err))  # type:ignore
            return None

        return response

    def _build_url_exact(self, q: str, **kwargs: Dict) -> str:
        """ build the parameters to make valid url
            returns a OrderedDict """
        url = f"{self._URL}?where="
        if kwargs.get('doi'):
            input_doi = kwargs.get('doi')
            url += f'''{{"doi":"{input_doi}"}}'''
        return url


def get_publication_from_id_in_db(new_id: str) -> Union[None, Dict]:

    """ Returns True if the id is already in the mongo db """

    # db_publications = app.data.driver.db["publications"]
    # try:
    #    res = db_publications.find({"id": new_id}).limit(1).next()
    # except:
    #    res = None
    # return res

    url = BaseConfig.DATAESR_PUBLICATIONS_URL
    url += '?where={{"id":"{}"}}'.format(new_id)
    r = requests.get(url)
    if r.status_code == 200:
        res = r.json()['data']
    else:
        res = []
    if len(res) > 1:
        print("ERROR more than one id - SHOULD NOT HAPPEN !!")
        return res[0]
    elif len(res) == 1:
        return res[0]
    else:
        return None


def get_publication_html_from_id_in_db(new_id: str) -> Union[None, Dict]:
    """ Returns True if the id is already in the mongo db """

    # db = app.data.driver.db["notices_publications"]
    # try:
    #    res = db.find({"id": new_id}).limit(1).next()
    # except:
    #    res = None
    # return res

    url = BaseConfig.DATAESR_NOTICES_PUBLICATIONS_URL
    url += '?where={{"id":"{}"}}'.format(new_id)
    r = requests.get(url)
    if r.status_code == 200:
        res = r.json()['data']
    else:
        res = []
    if len(res) > 1:
        print("ERROR more than one id - SHOULD NOT HAPPEN !!")
        return res[0]
    elif len(res) == 1:
        return res[0]
    else:
        return None


if __name__ == '__main__':
    test = DataESRPublication("VEBER")
    print(len(test.result))
