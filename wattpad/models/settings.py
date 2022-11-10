import jsonobject

class Settings(jsonobject.JsonObject):
    Token = jsonobject.StringProperty(default="")
    PublicLogChannel = jsonobject.StringProperty(default="")
    LogChannel = jsonobject.StringProperty(default="")


