from dataclasses import dataclass
from datetime import datetime


@dataclass
class Server:
    ServerId:int=0
    GuildId:str=""
    IsActive:int=0
    RegisteredOn:datetime=datetime.utcnow()