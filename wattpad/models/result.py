from dataclasses import dataclass
from datetime import datetime

@dataclass
class Result:
    IsSuccess: bool = False
    ResultInfo: str = ""

@dataclass
class ResultValidateUrl(Result):
    InvalidUrl: bool = False
    PatternMatched: bool = True

@dataclass
class ResultFollow(ResultValidateUrl):
    AlreadyFollowing: bool = False

@dataclass
class ResultNewUpdate(Result):
    NewUpdate: str = ""
    UpdatedDate: datetime = datetime.utcnow()

