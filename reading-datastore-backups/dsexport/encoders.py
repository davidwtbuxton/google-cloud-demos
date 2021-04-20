import base64
import json

from google.cloud.ndb import _legacy_entity_pb as entity_pb


class EntityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, entity_pb.PropertyValue_ReferenceValuePathElement):
            id_or_name = obj.id() if obj.has_id() else obj.name()
            return obj.type(), id_or_name
        elif isinstance(obj, entity_pb.PropertyValue_PointValue):
            return obj.x(), obj.y()
        elif isinstance(obj, entity_pb.PropertyValue_ReferenceValue):
            return {
                'app': obj.app(),
                'name_space': obj.name_space(),
                'database_id': obj.database_id(),
                'pathelement_list': obj.pathelement_list(),
            }
        elif isinstance(obj, entity_pb.PropertyValue_UserValue):
            return {
                'email': obj.email(),
                'auth_domain': obj.auth_domain(),
                'obfuscated_gaiaid': obj.obfuscated_gaiaid(),
            }

        return super().default(obj)


class UTF8BytesEncoder(EntityEncoder):
    """Assume any bytes object is a UTF-8 unicode string."""

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')

        return super().default(obj)


class Base64BytesEncoder(EntityEncoder):
    """Encode any bytes object as base64 ASCII string."""

    def default(self, obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('ascii')

        return super().default(obj)


class IgnoreBytesEncoder(EntityEncoder):
    """Assume bytes are UTF-8 encoded, return None if not."""

    def default(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return None

        return super().default(obj)


JSON_ENCODERS = {
    'utf-8': UTF8BytesEncoder,
    'base64': Base64BytesEncoder,
    'ignore': IgnoreBytesEncoder,
}
