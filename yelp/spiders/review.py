import json
import scrapy
from yelp.items import Review
from pymongo import MongoClient


URL = "https://www.yelp.com/search?find_desc={category}&find_loc={location}&ns=1&start={page}"
CATEGORY = "Restaurants"
LOCATION = "Tucson"

class YelpSpider(scrapy.Spider):
    name = "review"
    # collection_name = name
    def __init__(self):
        self.db = MongoClient()

        # self.mongo_uri = 'mongodb://localhost:27017'
        # self.mongo_db = 'scrapy'
        # self.mongo_db = MongoClient(self.mongo_uri)[self.mongo_db]
        # import ipdb; ipdb.set_trace()
        # self.client = MongoClient(self.mongo_uri)
        # self.db = self.client[self.mongo_db]

        self.items = self.db.scrapy.yelp.find()

        self.urlist = []
        for item in self.items:
            self.urlist += [ f"https://www.yelp.com{item['url']}?start={page}" for page in range(0, item["reviewCount"]//10*10 + 1, 20)]

        self.start_urls = self.urlist

    def parse(self, response):
        try:
            reviews = json.loads(response.css('script[type*="application/ld+json"]').getall()[-1].strip('<script type="application/ld+json">').strip('\n'))["review"]
            url = response.url.strip('https://www.yelp.com')
            for rv in reviews:
                review = Review(url = url, ratingValue = rv["reviewRating"]["ratingValue"], datePublished = rv["datePublished"])
                yield review


        except Exception as e: 
            e.with_traceback
            print(e)
