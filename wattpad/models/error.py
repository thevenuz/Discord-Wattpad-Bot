import jsonobject
from datetime import datetime


class Error(jsonobject.JsonObject):
    ErrorMessage = jsonobject.StringProperty(default="")
    ErrorTime = jsonobject.DateTimeProperty(default=datetime.utcnow())
