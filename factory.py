from source.thairath import Thairath
from source.sanook import Sanook
from source.posttoday import Posttoday
from source.blognone import Blognone

builders = {
    'thairath': Thairath,
    'sanook': Sanook,
    'posttoday': Posttoday,
    'blognone': Blognone
}
    
def scrape():
    for builder in builders:
        print(f"[{builder.upper()}] Scraping...")
        builders[builder]().insertDB()

if __name__ == "__main__":
    scrape()