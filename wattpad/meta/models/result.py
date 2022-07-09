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
class ResultUnfollowStory(Result):
    IsInvalidTitle:bool=False
    UnknownError:bool=False
    NotFollowing:bool=False

@dataclass
class ResultCheckStories(Result):
    StoryData:List[Story]= None
    IsEmpty:bool= False