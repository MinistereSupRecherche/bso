"""JSON encoding module."""
import os
from datetime import datetime
# import dateutil.parser
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from app.config import BaseConfig



class CustomJSONEncoder(JSONEncoder):
    """Redefine default JSON encoder."""

    def default(self, obj):
        """Default."""
        try:
            if isinstance(obj, datetime):
                return obj.strftime(BaseConfig.DATETIME_FORMAT)
            elif isinstance(obj, ObjectId):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def scanr_encoder(obj):
    """Scanr Encoder."""
    try:
        if isinstance(obj, datetime):
            return obj.strftime(BaseConfig.DATETIME_FORMAT_SCANR)
        elif isinstance(obj, ObjectId):
            return str(obj)
    except TypeError:
        pass
