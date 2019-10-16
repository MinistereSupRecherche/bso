"""Utils for correctly storing celery results in Mongo backend."""
import datetime
from app.utils.logger import create_logger
from celery.backends.mongodb import MongoBackend

logger = create_logger(__name__)


def configure_celery(app, celery):
    """Configure celery to access Flask's app_context()."""
    # set broker url and result backend from app config
    logger.info("Configuring Celery...")
    celery.conf.broker_url = app.config["CELERY_BROKER_URI"]
    celery.conf.result_backend = app.config["CELERY_RESULT_URI"]
    celery.conf.worker_log_format = app.config["LOGGER_FORMAT"]
    celery.conf.worker_task_log_format = (
        app.config["CELERY_TASK_LOGGER_FORMAT"])
    celery.conf.mongodb_backend_settings = {
        "taskmeta_collection": app.config["TASKS_COLLECTION_NAME"]}
    logger.info(f"Celery broker is now {celery.conf.broker_url}")
    logger.info(f"Celery backend is now {celery.conf.result_backend}")

    # rewrite default celery encoder so mongo encodes results himself
    MongoBackend.encode = celery_mongo_encoder
    MongoBackend._store_result = store_celery_results_in_mongo

    # Provide app context to celery worker
    TaskBase = celery.Task

    class AppContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

        def create_task(self, state="PROGRESS", result=None):
            self.backend._store_result(
                self.request.id, state=state, result=None,
                task_name=self.name,
                created_at=datetime.datetime.utcnow()
            )

    celery.Task = AppContextTask
    # run finalize to process decorated tasks
    celery.finalize()


def store_celery_results_in_mongo(
        self, task_id, result, state, created_at=None,
        task_name=None, traceback=None, request=None, **kwargs):
    """Rewrite results."""
    now = datetime.datetime.utcnow()
    actual = None
    meta = {
        'status': state,
        'result': result,
        'id': task_id,
        '_id': task_id,
        'modified_at': now
    }
    if created_at:
        meta['created_at'] = now
    if task_name:
        meta['name'] = task_name
    if state != "PROGRESS":
        actual = self.collection.find_one({"_id": task_id}) or {}
        actual.update(meta)
        actual['ended_at'] = now
        if actual.get("created_at"):
            actual["duration"] = (now-actual["created_at"]).total_seconds()
        meta = actual.copy()
    try:
        self.collection.save(meta)
    except Exception as exc:
        raise Exception(exc)

    return result


def celery_mongo_encoder(self, data):
    """Prevent celery to json.dumps results before sending it to mongo."""
    return data
