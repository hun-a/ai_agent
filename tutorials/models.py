from pydantic import BaseModel
from typing import List

class SubSection(BaseModel):
    title: str
    content: str

class BlogPost(BaseModel):
    title: str
    introduction: str
    sections: List[SubSection]
    sources: List[str]
    hashtags: List[str]