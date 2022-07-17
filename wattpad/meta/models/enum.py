import enum

class CustomMsgType(enum.Enum):
    Author="a"
    Story="s"

class HelpCategory(enum.Enum):
    Story="story"
    Author="author"
    Channel="channel"
    CustomMsg="custom message"
    CustomChannel="custom channel"
    Setup="setup"
    About="about"
