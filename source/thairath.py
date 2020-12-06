from .scraper import XmlScraper
import datetime as dt
from tqdm import trange
import time
import random
from bs4 import BeautifulSoup
import dateparser as dp
import pytz

class Thairath(XmlScraper):
    
    def __init__(self):
        super().__init__(
            "https://www.thairath.co.th/sitemap-daily.xml",
            "thairath"
        )
        self.tz = pytz.timezone('Asia/Bangkok')
    
    def execute(self):
        NS = {
            's': "http://www.sitemaps.org/schemas/sitemap/0.9", 
            'image':"http://www.google.com/schemas/sitemap-image/1.1"
        }
        parsed_elements = self.lxml_xpath("//s:url/s:loc | //image:image/image:loc | //image:image/image:title | //image:image/image:caption", namespaces=NS)
        news_data = []
        latest_url = self.getLatestUrl()

        for i in trange(int(len(parsed_elements)/4)):
            news_url, img_url, title  = parsed_elements[(i*4)].text, parsed_elements[(i*4)+1].text, parsed_elements[(i*4)+2].text

            if latest_url is not None and news_url == latest_url:
                print(f"[{self.publisher.upper()}] Duplicate found. Stopping...")
                break

            url_split = news_url.split("/")
            category = url_split[4] if url_split[3] == "news" else url_split[3]
            timestamp = self.getDate(news_url, category)  # Parse data for Thairath, as date is not given in XML

            if timestamp is None:
                print(f"[{self.publisher.upper()}] Timestamp is parsed None at {news_url}. Skipping...")
                continue

            time.sleep(5+(5*random.random()))
            news_data.append((news_url, img_url, category, timestamp, title, self.publisher))

        insert_query = """INSERT INTO news_source (url, img, category, timestamp, title, publisher) VALUES (%s, %s, %s, %s, %s, %s)"""
        return insert_query, news_data
    
    def getDate(self, url:str, category:str): 
        try:
            res = self.get_request(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            if category == "foreign" or category == "tech":
                date = soup.find("h3", {"class":["16shodj", "efr6tej3"]}).span.string
            else:
                date = soup.find("span", {"class":["css-x2q8w", "e1ui9xgn2"]}).string
            # tags = [tag.text for tag in soup.find("div", {"class": ["css-sq8bxp","evs3ejl16"]}).find_all("a")]

            dateparser = dp.date.DateDataParser(
                languages=['th'],
                locales=['th'],
            )

            parsed_date = dateparser.get_date_data(date, ["%d %b %y %H:%M น."])['date_obj']
            parsed_date = parsed_date.replace(year=parsed_date.year-543)
            return self.tz.localize(parsed_date)
        
        except AttributeError as e:
            print(e)

if __name__ == "__main__":
    scraper = Thairath()
    print(scraper.execute())