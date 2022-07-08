from dataclasses import dataclass

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