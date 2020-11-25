from .scraper import XmlScraper
import datetime as dt
from .news_utils import strip_text

class Posttoday(XmlScraper):
    
    def __init__(self):
        super().__init__( 
            [
                "http://www.posttoday.com/rss/src/politics.xml",
                "http://www.posttoday.com/rss/src/world.xml",
                "http://www.posttoday.com/rss/src/entertainment.xml",
                "http://www.posttoday.com/rss/src/lifestyle.xml"
            ],
            "posttoday"
        )
    
    def execute(self):
        news_data = []
        for rss_url in self.url:
            category = str(rss_url.split('/')[-1][:-4])
            parsed_elements = self.lxml_xpath("//item/title | //item/link | //item/description | //item/pubDate", url=rss_url)
            latest_url = self.getLatestUrl("SELECT url FROM news_source WHERE publisher=%s AND category=%s ORDER BY timestamp DESC LIMIT 1;", (self.publisher, category))

            for i in range(int(len(parsed_elements)/4)):
                title = strip_text(parsed_elements[(i*4)].text)
                news_url = strip_text(parsed_elements[(i*4)+1].text)
                caption = strip_text(parsed_elements[(i*4)+2].text)
                time = strip_text(parsed_elements[(i*4)+3].text)
                timestamp = dt.datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %z")
                if latest_url is not None and news_url == latest_url:
                    print(f"[{self.publisher.upper()}] Duplicate found. Stopping...")
                    break
                news_data.append((news_url, category, timestamp, title, self.publisher))

        insert_query = """ INSERT INTO news_source (url, category, timestamp, title, publisher) VALUES (%s, %s, %s, %s, %s)"""
        return insert_query, news_data

if __name__ == "__main__":
    scraper = Posttoday()
    print(scraper.execute())