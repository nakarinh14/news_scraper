from .scraper import XmlScraper
import datetime as dt

class Sanook(XmlScraper):
    
    def __init__(self):
        super().__init__(
            "https://www.sanook.com/news/sitemap/today/",
            "sanook"
        )
        
    def execute(self):
        NS = {
            's': "http://www.sitemaps.org/schemas/sitemap/0.9", 
            'image':"http://www.google.com/schemas/sitemap-image/1.1", 
            'news':"http://www.google.com/schemas/sitemap-news/0.9"
            }
        parsed_elements = self.lxml_xpath("//s:url/s:loc | //news:publication_date | //news:news/news:title | //image:image/image:loc", namespaces=NS)
        news_data = []
        latest_url = self.getLatestUrl()
        for i in range(int(len(parsed_elements)/4)):
            news_url, time, title, img_url = parsed_elements[(i*4)].text, parsed_elements[(i*4)+1].text, parsed_elements[(i*4)+2].text, parsed_elements[(i*4)+3].text
            category = ''
            timestamp = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
            if latest_url is not None and news_url == latest_url:
                print(f"[{self.publisher.upper()}] Duplicate found. Stopping...")
                break
            news_data.append((news_url, img_url, category, timestamp, title, self.publisher))

        insert_query = """ INSERT INTO news_source (url, img, category, timestamp, title, publisher) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
        return insert_query, news_data    

if __name__ == "__main__":
    scraper = Sanook()
    print(scraper.execute())