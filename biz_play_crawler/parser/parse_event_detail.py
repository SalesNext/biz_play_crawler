from collections.abc import Iterable
from biz_play_crawler.schema.biz_play_event import *
from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from urllib.parse import urlparse

def parse_event_detail(event :CrawlEvent[None, Event, HtmlResponse],
                       response: HtmlResponse) -> Iterable[Event]:
    
    data = BizPlayEvent()
    parsed_url = urlparse(response.url)
    path_parts = parsed_url.path.split('/')
    data.event_id = path_parts[-1]
    data.source_event_url = response.url
    data.event_name = response.xpath("//h1/text()").get()
    
    breadcrumb_urls = response.xpath("//a[@itemprop='item']/@href").getall()
    category_urls = [id for id in breadcrumb_urls if '/category/' in id]
    category_url = category_urls[-1]
    try:
        category_url = category_urls[-1]
    except IndexError:
        category_url = None 
    category_text = response.xpath(f"//a[@itemid='{category_url}']/span/text()").get()
    data.event_category = Category(text=category_text, href=category_url)
    print(category_url)
    video_title = response.xpath("//span[@class='title mr-2']/text()").getall()
    video_timeline = response.xpath("//span[@class='time']/text()").getall()
    
    event_video_content = []
    for title, time_at in zip(video_title, video_timeline):
        event_video_content.append(VideoTimeLine(title=title, time_at=time_at))
    data.event_video_content = event_video_content if event_video_content else None
    
    description_title =  " ".join(response.xpath("normalize-space(//div[@class='description']//strong//text())").getall())
    description_content = " ".join(response.xpath("//div[@class='description']//p//text()").getall())
    data.event_description = Description(title=description_title, content=description_content)
    
    data.event_company_name = response.xpath("//li[@class='company']/div/text()").get()
    
    instructors = response.xpath("//div[@class='instructor']/div[@class='profile-text text-gray-200']")
    instructor_list = []
    for instructor in instructors:
        corporate = instructor.xpath("./div[1]/text()").get()
        position = instructor.xpath("./div[2]/text()").get()
        name = instructor.xpath("./div[3]/text()").get()
        description = " ".join(instructor.xpath("./div[4]//p/text()").getall())
        instructor_list.append(Speaker(corporate=corporate, position=position, name=name, description=description))
    data.event_speaker = instructor_list if instructor_list else None
    
    related_url = list(set(response.xpath("//div[@class='wrapper']//a/@href").getall()))
    related_url = [url for url in related_url if not any(domain in url for domain in ["facebook.com", "twitter.com","#","b.hatena.ne.jp"])]
   
    book_information = response.xpath("//div[@class='book']/div[@class='information']")
    if book_information is not None:
        for book in book_information:
            book_title = book.xpath(".//div[@class='title']//h2/text()").get()
            author = book.xpath(".//div[@class='subtitle author']//h2/text()").get()
            publish_date = book.xpath(".//div[@class='subtitle publication-date']/text()").get().replace("発売日：", "").strip()
            publisher = book.xpath(".//div[@class='subtitle manufacturer']/text()").get().replace("出版社：", "").strip()
            order_link = related_url
            data.event_book_information = BookInformation(book_title=book_title, author=author, publish_date=publish_date, publisher=publisher, order_link=order_link)
            data.event_related_url = None
    else:
        data.event_related_url = related_url
        data.event_book_information = None
    
    other_seminar_urls = list(set(response.xpath("//section[@class='sidebar-seminars']//a/@href").getall()))
    
    for other_url in other_seminar_urls:
        yield CrawlEvent(
            request = Request(other_url),
            metadata = None,
            callback = parse_event_detail,
        )
    yield DataEvent("event_detail", data)
    
    
    
