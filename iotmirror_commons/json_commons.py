import json
import uuid
from datetime import datetime

class ObjectJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, uuid.UUID):
      return str(obj)
    if isinstance(obj, datetime):
      return obj.isoformat()
    if hasattr(obj, '__dict__'):
      return obj.__dict__
    return json.JSONEncoder.default(self, obj)