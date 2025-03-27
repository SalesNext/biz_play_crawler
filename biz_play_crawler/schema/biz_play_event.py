from pydantic import BaseModel
from typing import Optional, List



class VideoTimeLine(BaseModel):
    title: Optional[str] = None
    time_at: Optional[str] = None
 
class Speaker(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None



class BizPlayEvent(BaseModel):
    event_id: Optional[str] = None
    source_event_url: Optional[str] = None
    event_name: Optional[str] = None
    event_category : Optional[dict] = None
    event_video_content: Optional[List[VideoTimeLine]] = None
    event_description_title: Optional[str] = None
    event_description_content: Optional[str] = None
    event_company_name: Optional[str] = None
    event_speaker: Optional[List[Speaker]] = None
    event_related_url: Optional[List[str]] = None
  
    event_book_title: Optional[str] = None
    event_book_author: Optional[str] = None
    event_book_publish_date: Optional[str] = None
    event_book_publisher: Optional[str] = None
    event_book_order_link: List[str] = None
  