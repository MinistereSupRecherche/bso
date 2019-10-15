"""Swagger maker."""
from eve_swagger.swagger import index

from app.utils.logger import create_logger
from app.extensions import rp

logger = create_logger(__name__)


def generate_swagger():
    """Generate service documentation from Eve and RestPlus."""
    rest = rp.__schema__
    eve = index().get_json()
    doc = {"swagger": "2.0"}
    paths = {k: v for k, v in eve["paths"].items()}
    for k, v in rest["paths"].items():
        if k not in paths:
            paths.update({k: v})
        elif k in paths:
            logger.info(paths[k])
            logger.info(v)
            paths[k].update(v)
    doc["tags"] = eve["tags"]
    for e in rest.get('tags'):
        if e not in doc["tags"]:
            doc["tags"].append(e)
    doc["paths"] = paths
    doc["info"] = eve["info"]
    doc["basePath"] = eve["basePath"]
    doc["consumes"] = rest["consumes"]
    doc["produces"] = rest["produces"]
    doc["schemes"] = eve["schemes"]
    doc["definitions"] = rest.get("definitions") or {}
    for k, v in eve["definitions"].items():
        doc["definitions"][k] = v
    doc["parameters"] = eve["parameters"]
    return doc
