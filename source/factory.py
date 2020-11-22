from thairath import Thairath
from sanook import Sanook
from posttoday import Posttoday
from blognone import Blognone

class ScraperFactory:
    
    builders = {
        # 'thairath': Thairath,
        'sanook': Sanook,
        'posttoday': Posttoday,
        'blognone': Blognone
    }

    def build(self, publisher:str):
        print("Building scraper: " + publisher)
        self.builders[publisher]().insertDB()

    def buildAll(self):
        for builder in self.builders:
            self.build(builder)

if __name__ == "__main__":
    factory = ScraperFactory()
    factory.buildAll()