from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from wattpad.db.models.story import Story
from wattpad.meta.models.checkcustomchannels import AuthorCustomChannel, CheckCustomMsgAuthor, CheckCustomMsgStory, StoryCustomChannel

@dataclass
class Result:
    IsSuccess:bool=False
    ResultInfo:str=""

@dataclass
class ResultStory(Result):
    IsInvalidUrl:bool=False
    HasPattern:bool=True
    AlreadyFollowing:bool=False

@dataclass
class ResultUnfollow(Result):
    IsInvalidTitle:bool=False
    UnknownError:bool=False
    NotFollowing:bool=False
    HasMultipleStories:bool= False

@dataclass
class ResultCheck(Result):
    Data:List[Story]= None
    IsEmpty:bool= False

@dataclass
class ResultAuthor(Result):
    IsInvalidUrl:bool=False
    HasPattern:bool=True
    AlreadyFollowing:bool=False

@dataclass
class ResultPermissionsCheck(Result):
    HasReadPerms:bool= False
    HasSendPerms:bool= False
    HasEmbedPerms:bool= False

@dataclass
class ResultUnset(Result):
    NoChannelFound:bool= False

@dataclass
class ResultCustomChannelSet(Result):
    IsInvalidTitle:bool=False
    UnknownError:bool=False
    HasMultipleResults:bool= False
    Name:str=""
    

@dataclass
class ResultCustomChannelUnset(Result):
    IsInvalidTitle:bool=False
    UnknownError:bool=False
    HasMultipleResults:bool= False
    Notfound:bool= False

@dataclass 
class ResultCheckCustomChannel(Result):
    StoryCustomChannels:List[StoryCustomChannel]=field(default_factory=list)
    AuthorCustomChannels:List[AuthorCustomChannel]=field(default_factory=list)
    IsEmpty:bool = False

@dataclass 
class ResultCheckCustomMsg(Result):
    StoryCustomMsgs:List[CheckCustomMsgStory]=field(default_factory=list)
    AuthorCustomMsgs:List[CheckCustomMsgAuthor]=field(default_factory=list)
    IsEmpty:bool = False

@dataclass
class ResultNewUpdate(Result):
    NewUpdate:str=""
    UpdatedDate:datetime=datetime.utcnow()


