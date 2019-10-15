# """Config tester."""
# import unittest
# from flask import json
# from app.tests.base import BaseTestCase
# from app.tests.mocks.persons import mock_persons
# from app.api.custom.controllers import make_service_documentation
# from app.api.utils.logger import create_logger
#
# logger = create_logger(__name__)
#
#
# class TestPersonsRoute(BaseTestCase):
#     """Tests for celery and flask configs for Dev, Prod and Test."""
#
#     def test_persons(self):
#         """Ensure the /healthy route behaves correctly."""
#         response = self.client.get('/persons/healthy')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(True, data['message'])
#
#     def test_doc_eve(self):
#         """Ensure the /swagger route behaves correctly."""
#         response = self.client.get('/api-docs')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual("2.0", data['swagger'])
#         self.assertIn("paths", data.keys())
#         self.assertIn("/persons", data["paths"].keys())
#
#     def test_doc_restplus(self):
#         """Ensure the /swagger route behaves correctly."""
#         response = self.client.get('/persons/swagger.json')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual("2.0", data['swagger'])
#         self.assertIn("paths", data.keys())
#         self.assertIn("/healthy", data["paths"].keys())
#         self.assertIn("/swagger", data["paths"].keys())
#         self.assertIn("/dbstats", data["paths"].keys())
#         self.assertIn("""/identifiers/{collection}""", data["paths"].keys())
#         self.assertIn("/persons/autocomplete", data["paths"].keys())
#         self.assertIn("/tasks/infos", data["paths"].keys())
#         self.assertIn("/tasks", data["paths"].keys())
#
#     def test_doc_full(self):
#         """Ensure the full doc is built correctly."""
#         with self.client:
#             reve = self.client.get('/api-docs')
#             eve = json.loads(reve.data.decode())
#             self.assertEqual(reve.status_code, 200)
#             rrest = self.client.get('/persons/swagger.json')
#             rest = json.loads(rrest.data.decode())
#             self.assertEqual(rrest.status_code, 200)
#             doc = make_service_documentation(eve, rest)
#             self.assertEqual("2.0", doc['swagger'])
#             self.assertIn("paths", doc.keys())
#             self.assertIn("/healthy", doc["paths"].keys())
#             self.assertIn("/swagger", doc["paths"].keys())
#             self.assertIn("/dbstats", doc["paths"].keys())
#             self.assertIn("""/identifiers/{collection}""", doc["paths"].keys())
#             self.assertIn("/persons/autocomplete", doc["paths"].keys())
#             self.assertIn("/tasks/infos", doc["paths"].keys())
#             self.assertIn("/tasks", doc["paths"].keys())
#
#     def test_post_person_single(self):
#         """Ensure post route behaves correctly for a single document."""
#         single = mock_persons[1]
#         with self.client:
#             response = self.client.post(
#                 '/persons',
#                 json=single)
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             self.assertEqual("OK", data['status'])
#             self.assertEqual("idref183975154", data["id"])
#
#     def test_post_person_bulk(self):
#         """Ensure post route behaves correctly for bulk insert."""
#         with self.client:
#             response = self.client.post(
#                 '/persons',
#                 json=mock_persons)
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             self.assertEqual("OK", data['status'])
#             self.assertEqual("idref230880436", data['data'][0]["id"])
#             self.assertEqual("OK", data['data'][0]["status"])
#             self.assertEqual("idref183975154", data['data'][1]["id"])
#             self.assertEqual("OK", data['data'][1]["status"])
#
#     def test_post_person_ensure_validation(self):
#         """Ensure validation is made before adding to database."""
#         person = mock_persons[0]
#         person["first_name"] = True
#         with self.client:
#             response = self.client.post(
#                 '/persons',
#                 json=person)
#             data = json.loads(response.data.decode())
#             self.assertEqual("ERR", data['status'])
#             person["first_name"] = "Sylvain"
#
#     def test_get_persons(self):
#         """Ensure dupplicated ids throw error."""
#         with self.client:
#             response = self.client.post(
#                 '/persons',
#                 json=mock_persons)
#             response = self.client.get('/persons')
#             data = json.loads(response.data.decode())
#             self.assertEqual(2, data['meta']['total'])
#
#     def test_post_person_duplicated(self):
#         """Ensure dupplicated ids throw error."""
#         with self.client:
#             self.client.post(
#                 '/persons',
#                 json=mock_persons)
#             response = self.client.post(
#                 '/persons',
#                 json=mock_persons[0])
#             data = json.loads(response.data.decode())
#             self.assertEqual("ERR", data['status'])
#             self.assertEqual(422, data['error']["code"])
#             self.assertIn("id", data['issues'].keys())
#             self.assertIn("id_idref", data['issues'].keys())
#             self.assertIn("Insertion failure", data['error']["message"])
#
#
# class TestPersonsMatchRoute(BaseTestCase):
#     """Tests for celery and flask configs for Dev, Prod and Test."""
#
#     def test_idref(self):
#         """Ensure the idref route behaves correctly."""
#         response = self.client.get('/persons/match/idref?q=frederic olland')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual("183975154", data['data'][0]['ppn_z'])
#         self.assertEqual("one_found", data['status'])
#         self.assertIn("olland", data['data'][0]['all'])
#
#     def test_idref_bad_query(self):
#         """Ensure the idref route behaves correctly."""
#         response = self.client.get('/persons/match/idref?q="frederic olland"')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 400)
#         self.assertIn("Cannot get response from idref", data["error"])
#
#     def test_idref_not_found(self):
#         """Ensure the idref route behaves correctly."""
#         response = self.client.get(
#             '/persons/match/idref?q=fraehezipasjfe ceznupis')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual("not_found", data['status'])
#
#     # def test_orcid(self):
#     #     """Ensure the orcid route behaves correctly."""
#     #     response = self.client.get(
#     #         '/persons/match/orcid?first_name=frédéric&last_name=olland')
#     #     data = json.loads(response.data.decode())
#     #     logger.info(data)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(
#     #         "https://orcid.org/0000-0003-3459-2852",
#     #         data['data'][0]['id_orcid']
#     #     )
#     #     self.assertEqual("one_found", data['status'])
#
#
# if __name__ == "__main__":
#     unittest.main()
