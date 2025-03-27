from collections.abc import Iterable
from enum import Enum
from typing import Optional
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa
from biz_play_crawler.parser.parse_event_list import parse_event_list
from biz_play_crawler.parser.parse_event_list import CrawledEventIds


class BizPlayCrawler(ScrapyCrawler):
    def __init__(self, daily: bool = False) -> None:
        self.daily = daily
    
    def start(self) -> Iterable[Event]:
        crawled_event_ids = []
        if self.daily:
            crawled_event_ids : pa.Table = self.readers["event_detail"].read()
            crawled_event_ids = crawled_event_ids.select(["event_id"]).drop_null().to_pydict()["event_id"]
        for i in range(1,100):
            yield CrawlEvent(
                request = Request(url=f'https://biz-play.com/seminar/new?page={i}'),
                metadata= CrawledEventIds(crawled_event_ids = crawled_event_ids),
                callback=parse_event_list,
            )