"""RestPlus schemas."""
from flask_restplus import Model, fields, reqparse, inputs
from app.tasks import ALL_TASKS

processor = reqparse.RequestParser()
processor.add_argument(
    "processor", choices=["hal", "unpaywall"], required=True)

deleteBackend = reqparse.RequestParser()
deleteBackend.add_argument(
    'deleteBackend',
    type=inputs.boolean,
    default=False,
    help="if False only revokes the task, if True delete \
    the task from backend results storage. Default to False"
)

task_name = Model(
    "task_name", {
        "task_name": fields.String(
            choices=list(ALL_TASKS),
            description=f"One of {list(ALL_TASKS)}")
    }
)

hal_query = Model('hal_query', {
    "doi": fields.String(description='doi of a publication')
})

openapc_query = Model('openapc_query', {
    "doi": fields.String(description='doi of a publication'),
    "euro": fields.Float(description='apc'),
    "institution": fields.String(
        description='institution of affiliation of the publication'),
})

unpaywall_affiliation = Model('unpaywall_affiliation', {
    "name": fields.String(description='affiliation name')
    })

unpaywall_oa_location = Model('unpayall_oa_location', {
    "url": fields.String(description='url of the location'),
    "url_for_pdf": fields.String(description=''),
    "url_for_landing_page": fields.String(description=''),
    "license": fields.String(description=''),
    "version": fields.String(description=''),
    "host_type": fields.String(description=''),
    "evidence": fields.String(description=''),
    })

unpaywall_author = Model('unpaywall_author', {
    "given": fields.String(description='author first_name'),
    "family": fields.String(description='author last_name'),
    "affiliation": fields.List(fields.Nested(unpaywall_affiliation))
    })

unpaywall_query = Model('unpaywall_query', {
    "doi": fields.String(description='doi of a publication'),
    "updated": fields.String(description=''),
    "best_oa_location": fields.Nested(unpaywall_oa_location),
    "year": fields.Integer(description='year of the publication'),
    "genre": fields.String(description='genre of the publication'),
    "is_oa": fields.Boolean(description='bool is publi OA'),
    "title": fields.String(description='title of the publication'),
    "doi_url": fields.String(description='doi_url of the publication'),
    "journal_issns": fields.String(description='issns'),
    "journal_name": fields.String(description='journal name'),
    "publisher": fields.String(description='publisher of the publication'),
    "z_authors": fields.List(fields.Nested(unpaywall_author)),
    "journal_is_oa": fields.Boolean(description='journal is OA'),
    "journal_is_in_doaj": fields.Boolean(description='journal is in DOAJ'),
})
