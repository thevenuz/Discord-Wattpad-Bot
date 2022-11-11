import jsonobject
from datetime import datetime
from wattpad.models.error import Error


class Author(jsonobject.JsonObject):
    Url = jsonobject.StringProperty(default="", name="url")
    LastUpdated = jsonobject.StringProperty(default=datetime.utcnow(), name="lastupdated")
    CustomChannel = jsonobject.StringProperty(default="", name="CustomChannel")
    CustomMsg = jsonobject.StringProperty(default="", name="CustomMsg")
    Error = jsonobject.ObjectProperty(Error)
