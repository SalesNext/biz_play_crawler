

from collections.abc import Iterable

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from urllib.parse import urlparse
from biz_play_crawler.parser.parse_event_detail import parse_event_detail
import re
from typing import TypedDict

class CrawledEventIds(TypedDict):
    event_ids: list[str]
    
def parse_event_list(event :CrawlEvent[None, Event, HtmlResponse],
                       response: HtmlResponse) -> Iterable[Event]:
    
    event_urls = response.xpath("//a/@href").getall()
    pattern = r"https:\/\/biz-play\.com\/seminar\/\d+"
    valid_urls = [url for url in event_urls if re.match(pattern, url)]
    valid_urls = list(set(valid_urls))
    
    for url in valid_urls:
        
        yield CrawlEvent(
            request = Request(url),
            metadata = None,
            callback = parse_event_detail,
    )
    