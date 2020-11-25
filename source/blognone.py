from bs4 import BeautifulSoup
from .scraper import Scraper
import time
import random
import datetime as dt
import pytz

class Blognone(Scraper):

    def __init__(self):
        super().__init__("blognone")
        self.tz = pytz.timezone('Asia/Bangkok')
    
    def execute(self):
        base_url = "https://www.blognone.com/node?page="
        news_data, count = [], 0
        latest_url = self.getLatestUrl()
        curr_date = dt.datetime.now(self.tz)
        stop_execute = False
        while not stop_execute:
            res = self.get_request(base_url+str(count))
            soup = BeautifulSoup(res.text, 'html.parser')
            posts = soup.find("div", id="block-system-main").find_all("div", {"class": ["node","clearfix"]})
            for post in posts:
                # Get all the required information
                if(self.isSponsored(post)):
                    print("[BLOGNONE] Skipping Sponsored Post")
                    continue
                news_url, title, img_url, timestamp = self.parseNode(post)
                if (latest_url is not None and news_url == latest_url or (curr_date - timestamp).days >= 5):
                    print(f"[{self.publisher.upper()}] Duplicate found. Stopping...")
                    stop_execute = True
                    break
                news_data.append((news_url, img_url, "tech", timestamp, title, self.publisher))

            count += 1
            time.sleep(5+(5*random.random()))
        
        insert_query = """ INSERT INTO news_source (url, img, category, timestamp, title, publisher) VALUES (%s, %s, %s, %s, %s, %s)"""
        return insert_query, news_data
               
    def parseNode(self, node):
        title_box = node.find("div", class_="content-title-box")
        news_url = "https://www.blognone.com" + title_box.find("a")["href"]
        title = title_box.find("a").string
        img = node.find("div", class_="node-image").find("img")['src']
        date = node.find("span", class_="submitted").get_text().split("  on ")[1]
        parse_date = dt.datetime.strptime(date, "%d %B %Y - %H:%M").replace(tzinfo=self.tz)

        return news_url, title, img, parse_date
    def isSponsored(self, node):
        username = node.find("span", class_="username")
        return username.string in ["sponsored", "workplace"]

if __name__ == "__main__":
    scraper = Blognone()
    print(scraper.execute())