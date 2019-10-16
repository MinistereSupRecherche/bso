"""Async celery tasks definitions."""
from flask import json
from app.config import BaseConfig
from app.extensions import celery
from celery.utils.log import get_task_logger
from app.utils.mongo import mongo_connect, get_mongo
from app.utils.ftp import ftp_connect
from app.utils.json_encoding import scanr_encoder

from .ETLqueries import (
    authors_pipeline, publications_pipeline, organizations_pipeline)

logger = get_task_logger(__name__)

SCANR = BaseConfig.SCANR_COLLECTION_NAME
MAIN = BaseConfig.MAIN_COLLECTION_NAME


@celery.task(name='publications.send_scanr_to_prod', bind=True)
def send_scanr_to_prod(self):
    """Wrap send_scanr_to_ftp with dest option set as 'prod'."""
    logger.info("Task received. Sending scanr to prod...")
    self.create_task()
    return send_scanr_to_ftp(dest="prod")


@celery.task(name='publications.send_scanr_to_preprod', bind=True)
def send_scanr_to_preprod(self):
    """Wrap send_scanr_to_ftp with dest option set as 'preprod'."""
    logger.info("Task received. Sending scanr to prod...")
    self.create_task()
    return send_scanr_to_ftp(dest="preprod")


@mongo_connect
def send_scanr_to_ftp(mongo, dest):
    """Send scanr collection as a json file in ftp."""
    logger.info(f"Getting persons info from scanr database...")
    coll = mongo[SCANR]
    cursor = coll.find({}, {"_id": 0})

    # Creates a json file to send to ftp
    logger.info(f"Writing json file...")
    with open("temp.json", "w") as f:
        json.dump([cur for cur in cursor], f, default=scanr_encoder, indent=4)
        f.close()
    # Load the file and send it
    logger.info(f"Sending Scanr database to {dest} FTP...")
    with open("temp.json", "rb") as f:
        conn = ftp_connect(dest)
        conn.storbinary('STOR ' + BaseConfig.APP_NAME + '_v2.json', f)
    logger.info("Scanr database correctly sent to FTP")
    return {'ok': 1}


@celery.task(name='publications.etl_authors', bind=True)
@mongo_connect
def etl_authors(mongo, self):
    """ETL Authors.

    Extract from publications,
    Transform by aggregation
    Load to authors collection in the persons service.
    """
    self.create_task()
    mongo.drop_collection("authors")
    coll = mongo[MAIN]
    coll.aggregate(authors_pipeline, allowDiskUse=True)
    rename = {
        "renameCollection": 'publications.authors',
        "to": 'persons.authors',
        "dropTarget": True
    }
    client = get_mongo(level='client')
    client.admin.command(rename)
    return {"ok": 1}


@celery.task(name='publications.etl_organizations', bind=True)
@mongo_connect
def etl_organizations(mongo, self):
    """ETL Small publication for organizations.

    Extract from publications,
    Transform by aggregation
    Load to publications collection in the organizations service.
    """
    self.create_task()
    mongo.drop_collection("organizations")
    coll = mongo[MAIN]
    coll.aggregate(organizations_pipeline, allowDiskUse=True)
    rename = {
        "renameCollection": 'publications.organizations',
        "to": 'organizations.publications',
        "dropTarget": True
    }
    client = get_mongo(level='client')
    client.admin.command(rename)
    client.organizations.publications.create_index("affiliations")
    return {"ok": 1}


@celery.task(name='publications.etl_scanr', bind=True)
@mongo_connect
def etl_scanr(mongo, self):
    """ETL Authors.

    Extract from publications,
    Transform by reformating,
    Load to scanr collection.
    """
    self.create_task()
    coll = mongo[MAIN]
    coll.aggregate(publications_pipeline, allowDiskUse=True)
    return {"ok": 1}
