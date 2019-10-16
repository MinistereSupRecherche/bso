"""Custom Eve validators."""

import datetime
from bson import ObjectId
from eve.io.mongo import Validator


class CustomValidator(Validator):
    """Overwrite Eve Validator class."""

    def _validate_description(self, description, field, value):
        """{'type': 'string'}"""
        # Accept description attribute, used for swagger doc generation
        pass

    def _validate_example(self, example, field, value):
        """{'type': 'string'}"""
        # Accept description attribute, used for swagger doc generation
        pass

    def _normalize_default_setter_meta(self, document):
        meta = {
            "id": str(ObjectId()),
            "created_at": datetime.datetime.now(),
            "modified_at": datetime.datetime.now()
        }
        return meta

    def _normalize_coerce_meta(self, value):
        if not value.get('id'):
            value['id'] = str(ObjectId())
        if not value.get('created_at'):
            value['created_at'] = datetime.datetime.now()
        if not value.get('modified_at'):
            value['modified_at'] = datetime.datetime.now()
        return value

    def _normalize_default_setter_activity_status(self, document):
        if (not document.get('end_date')
                or document['end_date'] > datetime.datetime.now()):
            return 'active'
        else:
            return 'old'

    def _normalize_default_setter_strobjectid(self, document):
        return str(ObjectId())

    def _normalize_default_setter_utcnow(self, document):
        return datetime.datetime.now()
