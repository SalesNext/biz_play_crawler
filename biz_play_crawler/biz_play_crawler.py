from collections.abc import Iterable
from enum import Enum
from typing import Optional
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa
from biz_play_crawler.parser.parse_event_list import parse_event_list
from typing import TypedDict


class BizPlayCrawler(ScrapyCrawler):
    def __init__(self, daily: bool = False) -> None:
        self.daily = daily
    
    def start(self) -> Iterable[Event]:
        for i in range(1,100):
            yield CrawlEvent(
                request = Request(url=f'https://biz-play.com/seminar/new?page={i}'),
                metadata= None,
                callback=parse_event_list,
            )