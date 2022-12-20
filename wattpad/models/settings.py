from dataclasses import dataclass

@dataclass
class Settings():
    Token: str
    PublicLogChannel:str = ""
    LogChannel:str = ""


