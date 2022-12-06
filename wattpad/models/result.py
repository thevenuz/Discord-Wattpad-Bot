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

@dataclass
class ResultPermissionsCheck(Result):
    HasReadPerms: bool= False
    HasSendPerms: bool= False
    HasEmbedPerms: bool= False

@dataclass
class ResultSetChannel(Result):
    AlreadyExists: bool = False

@dataclass
class ResultUnsetChannel(Result):
    NoChannel: bool = False

@dataclass
class ResultSetCustomChannel(Result):
    NoStoryNameFound: bool = False
    NoStoryFound: bool = False
    MultipleStoriesFound: bool = False
    StoryName: str =""
    NoAuthorNameFound: bool = False
    NoAuthorFound: bool = False
    MultipleAuthorsFound: bool = False
    AuthorName: str = ""

@dataclass
class ResultUnsetCustomChannel(Result):
    NoStoryNameFound: bool = False
    NoStoryFound: bool = False
    MultipleStoriesFound: bool = False
    StoryName: str =""
    NoAuthorNameFound: bool = False
    NoAuthorFound: bool = False
    MultipleAuthorsFound: bool = False
    AuthorName: str = ""
