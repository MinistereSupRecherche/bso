"""Eve ressource definition."""
from .schemas import (publications_schema,
                      notices_publications_schema,
                      dump_unpaywall_schema,
                      dump_openapc_schema,
                      dump_opencitations_schema,
                      tasks_schema)

publications = {
    'url': 'publications',
    'schema': publications_schema,
    'mongo_indexes': {
      'docid': ([("id", 1)], {"unique": True}),
      'publication_date': ([("publication_date", 1)], {"background": True}),
      'genre': ([("genre", 1)], {"background": True}),
      'projects': ([("projects", 1)], {"background": True}),
      'is_french': ([("is_french", 1)], {"background": True}),
      'is_oa': ([("is_oa", 1)], {"background": True}),
      'authors_lastname': ([("authors.last_name", 1)], {
          "background": True, "collation": {"locale": "fr", "strength": 1}}),
      'link_type': ([("links.link_type", 1)], {"background": True}),
      'authors_id': ([("authors.id", 1)], {"background": True}),
      'oa_host_type': ([("oa_host_type", 1)], {"background": True}),
      'funding_ref': ([("funding_info.funding_ref", 1)], {"background": True}),
      'affiliations_id': ([("affiliations.id", 1)], {"background": True}),
      'authors_affiliations_id': ([("authors.affiliations.id", 1)], {"background": True}),
      'id_ext_type_value': ([("id_external.id_type", 1), ("id_external.id_value", 1)], {"background": True}),
      'is_french_publication_date': (
          [("is_french", 1), ("publication_date", 1), ("id", 1)], {"background": True}),
      'is_french_oa_publication_date': (
          [("is_french", 1), ("publication_date", 1), ("is_oa", 1), ("id", 1)], {"background": True}),
      'is_french_oa_host_type': (
          [("is_french", 1), ("oa_host_type", 1), ("id", 1)], {"background": True}),
      'is_oa_publication_date': (
          [("is_oa", 1), ("publication_date", 1), ("id", 1)], {"background": True}),
      'is_french_persons_identified_simple': (
          [("is_french", 1), ("persons_identified", 1)], {"background": True}),
      'is_french_persons_identified': (
          [("is_french", 1), ("id", 1), ("persons_identified", 1)], {"background": True}),
      'is_french_structures_identified': (
          [
            ("is_french", 1),
            ("id", 1),
            ("structures_identified", 1)
          ],
          {"background": True}
      ),
      'is_french_structures_identified_simple': (
          [
            ("is_french", 1),
            ("structures_identified", 1)
          ],
          {"background": True}
      ),
      'doi': (
        [("doi", 1)],
        {"partialFilterExpression": {
            "doi": {"$exists": True}},
            "unique": True,
            "background": True}),
      'text_index': ([
        ("doi", "text"),
        ("id_hal", "text"),
        ("title", "text"),
        ("summary", "text"),
        ("alternative_summary", "text"),
        ("authors.last_name", "text"),
        ("id_external.id_value", "text")],
        {
            "default_language": "en",
            "language_override": "en",
            "background": True}
       )
    }
}

tasks = {
    'item_title': "Tasks",
    'url': 'tasks',
    'allow_unknown': True,
    'hateoas': False,
    "resource_methods": ['GET'],
    "item_methods": ['GET'],
    'schema': tasks_schema
}

scanr = {
    'item_title': "scanR",
    'url': 'scanr',
    'allow_unknown': True,
    'hateoas': False,
    "resource_methods": ['GET'],
    "item_methods": ['GET'],
    'schema': tasks_schema
}

notices_publications = {
    'item_title': "notices_publications",
    'url': 'notices_publications',
    'schema': notices_publications_schema,
    'mongo_indexes': {
        'docid': ([("id", 1)], {"unique": True})
    },
    "hateoas": False
}

unpaywall_dump = {
    'item_title': "unpaywall_dump",
    'url': 'dumps_unpaywall',
    'allow_unknown': True,
    'hateoas': False,
    'id_field': "doi",
    'item_lookup_field': "doi",
    'schema': dump_unpaywall_schema,
    'mongo_indexes': {
        'id': ([("doi", 1)], {"unique": True}),
        'treated': ([("treated", 1)]),
        'year': ([("year", 1)]),
        'year_treated': ([("treated", 1), ("year", 1)]),
        'affiliation_treated': ([("z_authors.affiliation.name", 1), ("treated", 1)], {"background": True}),
#        'oa_locations_url': ([("oa_locations.url", 1)], {"background": True}),
        'published_date_history': (
          [("published_date", 1), ("oa_locations_history.is_oa", 1),
              ("oa_locations_history.updated", 1)], {"background": True})
#        ,'text_index': ([("$**", "text")])
    }
}

openapc_dump = {
    'item_title': "openapc_dump",
    'url': 'dumps_openapc',
    'allow_unknown': True,
    'hateoas': False,
    'id_field': "doi",
    'item_lookup_field': "doi",
    'schema': dump_openapc_schema,
    'mongo_indexes': {
        'id': ([("doi", 1)], {"unique": True}),
        'treated': ([("treated", 1)]),
        'period': ([("period", 1)]),
        'period_treated': ([("treated", 1), ("period", 1)]),
        'text_index': ([("$**", "text")])
    }
}

opencitations_dump = {
    'item_title': "opencitations_dump",
    'url': 'dumps_opencitations',
    'allow_unknown': True,
    'hateoas': False,
    'id_field': "oci",
    'item_lookup_field': "oci",
    'schema': dump_opencitations_schema,
    'mongo_indexes': {
        'id': ([("oci", 1)], {"unique": True, "background": True}),
        'cited': ([("cited", 1)], {"background": True}),
        'citing': ([("citing", 1)], {"background": True})
    }
}
