import json
import scrapy
from yelp.items import Place
from yelp.items import Review
from pymongo import MongoClient


URL = "https://www.yelp.com/search?find_desc={category}&find_loc={location}&ns=1&start={page}"
CATEGORY = "Restaurants"
LOCATION = "Tucson"

class YelpSpider(scrapy.Spider):
    name = "yelp"
    def __init__(self):
        self.pages = 990
        self.start_urls = [URL.format(category=CATEGORY, location=LOCATION, page=i) for i in range(0,self.pages,30)]

    def parse(self, response):
        if response.url.startswith("https://www.yelp.com/search"):
            try: 
                dic = {}
                infolist = json.loads(response.css('script[type*="application/json"]').getall()[1].split("<!--")[1].strip("--></script>"))['searchPageProps']
                
                mapinfo = infolist['searchMapProps']['mapState']['markers']
                resultinfo = infolist['searchResultsProps']['searchResults'] 

                for each in mapinfo:
                    if 'label' in each.keys():
                        index = int(each['label'])

                        small_dic = {}
                        
                        url = each["url"]
                        lat = each["location"]["latitude"]
                        lon = each["location"]["longitude"]
                        small_dic["url"] = url
                        small_dic["lat"] = lat
                        small_dic["lon"] = lon

                        dic[index] = small_dic

                for each in resultinfo:
                    if 'markerKey' in each.keys():
                        if each['markerKey'] in dic:
                            templist = []
                            for rsv_dlvry_info in each["searchActions"]:
                                descr = rsv_dlvry_info["content"]["text"]["text"]
                                templist.append(descr)

                            dic[each['markerKey']]["searchActions"] = templist

                            photo_info = each['scrollablePhotos']
                            dic[each['markerKey']]['allPhotosHref'] = photo_info['allPhotosHref']
                            dic[each['markerKey']]['photoHref'] = photo_info['photoList'][0]["src"]

                            business_result = each['searchResultBusiness']
                            dic[each['markerKey']]['reviewCount'] = business_result['reviewCount']
                            dic[each['markerKey']]['name'] = business_result['name']
                            dic[each['markerKey']]['rating'] = business_result['rating']
                            dic[each['markerKey']]['phone'] = business_result['phone']
                            dic[each['markerKey']]['rating'] = business_result['rating']
                            dic[each['markerKey']]['formattedAddress'] = business_result['formattedAddress']

                            templist = []
                            for categ_info in business_result['categories']:
                                templist.append(categ_info["title"])

                            dic[each['markerKey']]['categories'] = templist

                urlist = []
                for index, subdic in dic.items():
                    place = Place(url = subdic["url"], lat = subdic["lat"], lon = subdic["lon"], searchActions = subdic["searchActions"], allPhotosHref = subdic["allPhotosHref"], photoHref = subdic["photoHref"], reviewCount = subdic["reviewCount"], name = subdic["name"], rating = subdic["rating"], phone = subdic["phone"], formattedAddress = subdic["formattedAddress"], categories = subdic["categories"], reviews = {})
                    yield place

                    urlist += [ f"https://www.yelp.com{subdic['url']}?start={page}" for page in range(0, subdic["reviewCount"]//10*10 + 1, 20)]
                    for url in urlist:
                        yield scrapy.Request(url,meta=place, callback=self.parse)


            except Exception as e: 
                e.with_traceback
                print(e)

        elif response.url.startswith("https://www.yelp.com/biz"):
            self.db = MongoClient()
            self.collection = self.db.scrapy.yelp
            reviews = json.loads(response.css('script[type*="application/ld+json"]').getall()[-1].strip('<script type="application/ld+json">').strip('\n'))["review"]

            url = response.url.strip('https://www.yelp.com').split("?start=")[0]
            for rv in reviews:

                datePublished = rv["datePublished"]
                datePublished = " ".join(datePublished.split("-")[:2])
                if not url.startswith("/"):
                    url = "/" + url
                ratingValue = rv["reviewRating"]["ratingValue"]

                doc = self.collection.find_one({"url":url})
                try:
                    if datePublished in doc["reviews"]:
                        self.collection.find_one_and_update({"url":url}, { '$inc': { f"reviews.{datePublished}.count": 1} }, upsert=False)
                        existing_ratingValue = self.collection.find_one({"url":url})["reviews"][datePublished]["ratingValue"]
                        self.collection.find_one_and_update({"url":url}, { '$set': { f"reviews.{datePublished}.ratingValue": existing_ratingValue + ratingValue} }, upsert=False)
                    else:
                        self.collection.find_one_and_update({"url":url}, { '$set': { f"reviews.{datePublished}" : {"count" : 1, "ratingValue" : ratingValue}} })
                except Exception as e:
                    e.with_traceback
                    print(e)
                    print("doc:", doc)
            
