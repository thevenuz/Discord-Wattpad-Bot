from dataclasses import dataclass, field
from typing import List


@dataclass
class StoryCustomChannel:
    Channel:str=""
    Stories:List[str]= field(default_factory=list)

@dataclass
class AuthorCustomChannel:
    Channel:str=""
    Authors:List[str]=field(default_factory=list)

@dataclass
class CheckCustomMsgStory:
    Story:str=""
    Message:str=""


@dataclass
class CheckCustomMsgAuthor:
    Author:str=""
    Message:str=""