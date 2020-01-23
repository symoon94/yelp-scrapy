import json
import scrapy
from yelp.items import Place


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

                for index, subdic in dic.items():
                    place = Place(url = subdic["url"], lat = subdic["lat"], lon = subdic["lon"], searchActions = subdic["searchActions"], allPhotosHref = subdic["allPhotosHref"], photoHref = subdic["photoHref"], reviewCount = subdic["reviewCount"], name = subdic["name"], rating = subdic["rating"], phone = subdic["phone"], formattedAddress = subdic["formattedAddress"], categories = subdic["categories"])
                
                    yield place


            except Exception as e: 
                e.with_traceback
                print(e)
                import ipdb; ipdb.set_trace()

        # elif response.url.startswith("https://www.yelp.com/biz"):
            
        #     pass




# class YelpSpider(scrapy.Spider):
#     name = "yelp"
#     start_urls = ["https://www.yelp.com/biz/prep-and-pastry-tucson-7"]

#     def parse(self, response):
#         import ipdb; ipdb.set_trace()
#         try: 
#             import ipdb; ipdb.set_trace()
#             javascript = response.css('script::text').getall()
#             java = javascript[12].strip("<!--").strip("-->")
#             infolist = json.loads(java)['searchPageProps']['searchMapProps']['mapState']['markers']
#             for i in range(0,len(infolist)-2):
#                 url = "https://www.yelp.com" + infolist[i]["url"]
#                 import ipdb; ipdb.set_trace()
#                 yield {
#                     "url" : url,
#                     "lat" : infolist[i]["location"]["latitude"],
#                     "lon" : infolist[i]["location"]["longitude"]
#                 }



#         except:
                # TODO: debug 
                
#             reviews = json.loads(javascript.getall()[-1].strip('<script type="application/ld+json">').strip('\n'))["review"]
#             for i in range(len(reviews)):
#                 rating_val = reviews[i]["reviewRating"]["ratingValue"]
#                 date = reviews[i]["datePublished"]

#             # import ipdb; ipdb.set_trace()
#             print("error")
#              response.css('script[type*="applicatio
# n/json"]').getall()

