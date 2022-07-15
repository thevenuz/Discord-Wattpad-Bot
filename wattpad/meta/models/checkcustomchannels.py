from dataclasses import dataclass
from typing import List


@dataclass
class StoryCustomChannel:
    Channel:str=""
    Stories:List[str]=[]

@dataclass
class AuthorCustomChannel:
    Channel:str=""
    Authors:List[str]=[]

@dataclass
class CheckCustomMsgStory:
    Story:str=""
    Message:str=""


@dataclass
class CheckCustomMsgAuthor:
    Author:str=""
    Message:str=""