from dataclasses import dataclass
from datetime import datetime


@dataclass
class Channel:
    ChannelId:int=0
    Channel:str=""
    ServerId:int=0
    IsActive:int=0
    IsCustomChannel:int=0
    RegisteredOn:datetime=datetime.utcnow()