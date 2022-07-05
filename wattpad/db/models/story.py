from dataclasses import dataclass
from datetime import datetime

@dataclass
class Story:
    StoryId:int=0
    Url:str=""
    ServerId:int=0
    ChannelId:int=0
    IsActive:int=0
    LastUpdatedOn:datetime=datetime.utcnow()
    LastcheckedOn:datetime=datetime.utcnow()
    RegisteredOn:datetime=datetime.utcnow()