from dataclasses import dataclass
from datetime import datetime


@dataclass
class CustomMsg:
    MsgId:int=0
    Type:str=""
    Message:str=""
    StoryId:int=0
    AuthorId:int=0
    IsActive:int=0
    RegisteredOn:datetime=datetime.utcnow()