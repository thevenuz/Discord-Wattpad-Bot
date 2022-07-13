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