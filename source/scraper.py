from . import database as db
import requests
from lxml import etree
from math import ceil
# Abstract class for Scraper

class Scraper:
    
    def __init__(self, publisher:str):
        self.publisher = publisher
        self.headers= {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]"
        }
    def get_request(self, url):
        return requests.get(url, self.headers)

    def execute(self):
        # Interface. Override on extend
        return ("", [])

    def getLatestUrl(self, query:str = "SELECT url FROM news_source WHERE publisher=%s ORDER BY timestamp DESC LIMIT 1;", values:list = None):
        values = (self.publisher,) if values is None else values
        return db.findLatestUrl(query, values)

    def insertDB(self):
        insert_query, news_data = self.execute()
        if isinstance(insert_query, str):
            db.insert_batch(insert_query, news_data)
        elif isinstance(insert_query, list):
            n = insert_query[1]
            for batch in range(ceil(len(news_data) / n)):
                db.insert_batch(insert_query[0], news_data[batch*n : (batch+1)*n])

class XmlScraper(Scraper):
    
    def __init__(self, url:str, publisher:str):
        super().__init__(publisher)
        self.url = url   # Some news site have an .xml sitemap. 1 url will contain all daily news.

    def get_request(self, url):
        if url is None:
            return super().get_request(self.url)
        return super().get_request(url)

    def lxml_xpath(self, xpath:str, namespaces:dict=None, url=None):
        res = self.get_request(url)
        tree = etree.XML(res.content)
        if namespaces is not None:
            return tree.xpath(xpath, namespaces=namespaces)
        return tree.xpath(xpath)
    

    def execute(self):
        # Interface. Override on extend
        return (None, None)
