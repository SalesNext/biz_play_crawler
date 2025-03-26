from pydantic import BaseModel
from typing import Optional, List


class Category(BaseModel):
    text: Optional[str] = None
    href: Optional[str] = None
    
class VideoTimeLine(BaseModel):
    title: Optional[str] = None
    time_at: Optional[str] = None
 
class Description(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Speaker(BaseModel):
    corporate: Optional[str] = None
    position: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

class BookInformation(BaseModel):
    book_title: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    publisher: Optional[str] = None
    order_link: List[str] = None

class BizPlayEvent(BaseModel):
    event_id: Optional[str] = None
    source_event_url: Optional[str] = None
    event_name: Optional[str] = None
    event_category : Optional[Category] = None
    event_video_content: Optional[List[VideoTimeLine]] = None
    event_description: Optional[Description] = None
    event_company_name: Optional[str] = None
    event_speaker: Optional[List[Speaker]] = None
    event_related_url: Optional[List[str]] = None
    event_book_information: Optional[BookInformation] = None