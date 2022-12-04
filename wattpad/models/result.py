from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Result:
    IsSuccess: bool = False
    ResultInfo: str = ""
    UnknownError: bool = False

@dataclass
class ResultValidateUrl(Result):
    InvalidUrl: bool = False
    PatternMatched: bool = True

@dataclass
class ResultFollow(ResultValidateUrl):
    AlreadyFollowing: bool = False
    AuthorName: str = ""
    StoryName: str = ""

@dataclass
class ResultUnfollow(Result):
    AuthorNotFound: bool = False
    AuthorNameNotFound: bool = False
    StoryNotFound: bool = False
    StoryNameNotFound: bool = False

@dataclass
class ResultCheck(Result):
    Data: List = field(default_factory = list)

@dataclass
class ResultNewUpdate(Result):
    NewUpdate: str = ""
    UpdatedDate: datetime = datetime.utcnow()

