from dataclasses import dataclass
from typing import List
from wattpad.db.models.story import Story

@dataclass
class Result:
    IsSuccess:bool=False
    ResultInfo:str=""

@dataclass
class ResultStory(Result):
    IsInvalidUrl:bool=False
    HasPattern:bool=True

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
    

@dataclass
class ResultCustomChannelUnset(Result):
    Notfound:bool= False
