"""Flask endpoints for the API."""
from flask import json, jsonify, url_for, request  # type:ignore
from flask import current_app as app
from flask_restplus import Resource, abort  # inputs  # type:ignore
from pymongo.errors import OperationFailure

from app.extensions import rp, celery
from app.tasks import ALL_TASKS, TASKS_INFO
from app.utils.logger import create_logger
from app.analyzers import (UnpaywallPublication,
                           HALPublication,
                           PublicationUpdate)
from app.api.swagger import generate_swagger
from .models import (hal_query,
                     openapc_query,
                     unpaywall_affiliation,
                     unpaywall_oa_location,
                     unpaywall_author,
                     unpaywall_query,
                     task_name,
                     processor,
                     deleteBackend)

logger = create_logger(__name__)

# Namespace
analyzer = rp.namespace(
    'Analizers',
    path='/',
    description='Matchers to identify \
    persons and retrieve data from external or internal services'
)
ns0 = rp.namespace('Default', path='/')
ns1 = rp.namespace('Publication Processors', path='/')
ns2 = rp.namespace('Tasks', path='/')
ns3 = rp.namespace('Collection Tools', path='/')

rp.models[task_name.name] = task_name
rp.models[hal_query.name] = hal_query
rp.models[openapc_query.name] = openapc_query
rp.models[unpaywall_affiliation.name] = unpaywall_affiliation
rp.models[unpaywall_oa_location.name] = unpaywall_oa_location
rp.models[unpaywall_author.name] = unpaywall_author
rp.models[unpaywall_query.name] = unpaywall_query

# Response constants
NOT_FOUND = "NOT FOUND"
BAD_REQUEST = "BAD REQUEST"
UPDATED = "UPDATED"
CREATED = "CREATED"
OK = "SUCCESS"
UNKNOWN_TASK = "UNKNOWN TASK"


@ns0.route('/healthy')
class Healthy(Resource):
    """Organization service health route."""

    @ns0.response(200, OK)
    def get(self):
        """Health check route."""
        return {"message": True}, 200


@ns0.route('/swagger')
class SwaggerDocumentation(Resource):
    """Organization service documentation route."""

    @ns0.response(200, OK)
    def get(self):
        """Health check route."""
        doc = generate_swagger()
        return doc, 200


@ns0.route('/dbstats')
class DBStats(Resource):
    """Projects service database stats route."""

    @ns0.response(200, OK)
    def get(self):
        """Get statistics for all collections."""
        stats = {
            "database": app.data.driver.db.command("dbstats"),
            "collections": {}
        }
        collections = app.data.driver.db.collection_names()
        for coll in collections:
            coll_stat = app.data.driver.db.command("collstats", coll)
            for field in ["wiredTiger", "indexDetails"]:
                del coll_stat[field]
            stats['collections'].update({coll: coll_stat})
            stats = json.loads(json.dumps(stats))
        return {"data": stats}, 200


# ----------------- ns1 routes ----------------
@ns1.route('/_update')
class PublicationUpdater(Resource):
    """Update a publication."""

    @ns1.response(200, OK)
    @ns1.expect(unpaywall_query, validate=False)
    def post(self) -> None:
        """Update a publication."""
        q = rp.payload
        response = PublicationUpdate(q=None, **q)
        logger.debug("after update")
        logger.debug(response)
        return jsonify(  # type:ignore
            {
               "status": response.status
            }
        )


@ns1.route('/_process')
class PublicationProcessor(Resource):
    """Process a publication coming from HAL."""

    @ns1.response(200, OK)
    @ns1.expect(processor, unpaywall_query, validate=False)
    def post(self) -> None:
        """Process a publication coming from HAL."""
        args = processor.parse_args()
        q = rp.payload
        if args["processor"] == "hal":
            resp = HALPublication(**q)
        elif args["processor"] == "unpaywall":
            resp = UnpaywallPublication(**q)
        response = {"data": resp.result, "status": resp.status.lower()}
        return response, 200


# ----------------- ns3 routes ----------------
@ns3.route('/_distinct/<string:collection>/<string:field>')
class DistinctFieldValues(Resource):  # type:ignore
    """Update a publication."""

    @ns3.response(200, OK)  # type:ignore
    def get(self, collection, field):
        """Get all distinct values of a given field."""
        response = {
            "collection": collection, "field": field,
            "values": None, "count": None, "error": None}
        try:
            coll = app.data.driver.db[collection]
            nomenclature = coll.distinct(field)
            nom = json.loads(json.dumps(nomenclature))
            response.update({"values": nom, "count": len(nom)})
        except OperationFailure:
            response["error"] = "distinct too big"
            return response, 200
        except Exception:
            response["error"] = "An error occured."
        return response, 200


# ------------ Tasks Routes ----------------
@ns2.route('/tasks')
class CeleryTasks(Resource):
    """Export from ScanR to FTP."""

    @ns2.response(400, BAD_REQUEST)
    @ns2.response(201, CREATED)
    @ns2.expect(task_name)
    def post(self):
        """Post a new task."""
        task_name = rp.payload.get("task_name")
        task_to_execute = ALL_TASKS.get(task_name)
        if not task_to_execute:
            abort(404, message=UNKNOWN_TASK)
        t = task_to_execute.delay()
        location = url_for("tasks|resource", _external=True) + f"/{t.id}"
        response = {'data': {'task_id': t.id, "location": location}}
        return response, 201, {"Location": location}


@ns2.route('/tasks/<string:taskId>')
class CeleryTask(Resource):
    """Cancel a task."""

    @ns2.response(404, NOT_FOUND)
    @ns2.response(200, OK)
    def delete(self, taskId):
        """Cancel a task."""
        celery.control.revoke(taskId, terminate=True)
        if request.args.get("deleteBackend"):
            app.data.driver.db['tasks'].delete_one({'_id': taskId})
        return {}, 200


@ns2.route('/tasks/_infos')
class AvailableTasks(Resource):
    """Get all available tasks with execution infos."""

    @ns2.response(200, OK)
    @ns2.expect(deleteBackend)
    def get(self):
        """Get all available tasks."""
        return {"data": TASKS_INFO}, 200


# --------- analysers routes -----------
@analyzer.route('/update')
class AnalyzerPublicationUpdate(Resource):  # type:ignore
    """Update a publication."""

    @analyzer.response(404, "Nothing found")  # type:ignore
    @analyzer.expect(unpaywall_query, validate=False)  # type:ignore
    def post(self) -> None:
        """Update a publication."""
        q = rp.payload
        response = PublicationUpdate(q=None, **q)
        logger.debug("after update")
        logger.debug(response)
        return jsonify(  # type:ignore
            {
               "status": response.status
            }
        )


@analyzer.route('/hal_publication')
class AnalyzerHalPublication(Resource):  # type:ignore
    """Process a publication coming from HAL."""

    @analyzer.response(404, "Nothing found")  # type:ignore
    @analyzer.expect(hal_query, validate=False)  # type:ignore
    def post(self) -> None:
        """Process a publication coming from HAL."""
        q = rp.payload
        response = HALPublication(**q)

        return jsonify(  # type:ignore
            {
               "data": response.result,
               "status": response.status
            }
        )


@analyzer.route('/unpaywall_publication')
class AnalyzerUnpaywallPublication(Resource):  # type:ignore
    """Process a publication coming from unpaywall."""

    @analyzer.response(404, "Nothing found")  # type:ignore
    @analyzer.expect(unpaywall_query, validate=False)  # type:ignore
    def post(self) -> None:
        """Process a publication coming from unpaywall."""
        q = rp.payload
        response = UnpaywallPublication(**q)

        return jsonify(  # type:ignore
            {
               "data": response.result,
               "status": response.status
            }
        )

# @analyzer.route('/openapc_publication')
# class OpenAPCPublicationCheck(Resource): #type:ignore
#    """ Check if the publication is in HAL """
#
#    @analyzer.response(404, "Nothing found") #type:ignore
#    @analyzer.expect(hal_query, validate=True) #type:ignore
#    def post(self) -> None:
#
#        q = rp.payload
#        response = OpenAPCPublication(**q)
#
#        return jsonify( #type:ignore
#            {
#            "data": response.result,
#            "status":response.status
#            }
#        )
