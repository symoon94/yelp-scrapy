import json
import scrapy

# URL = "https://www.yelp.com/search?find_desc=&find_loc=tucson&ns=1&start={page}"

# class YelpSpider(scrapy.Spider):
#     name = "yelp"
#     start_urls = [URL.format(page=i) for i in range(0,1000,10)]

#     def parse(self, response):
#         try: 
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
#             # import ipdb; ipdb.set_trace()
#             print("error")




class YelpSpider(scrapy.Spider):
    name = "yelp"
    start_urls = ["https://www.yelp.com/biz/prep-and-pastry-tucson-7"]

    def parse(self, response):
        import ipdb; ipdb.set_trace()
        try: 
            import ipdb; ipdb.set_trace()
            javascript = response.css('script::text').getall()
            java = javascript[12].strip("<!--").strip("-->")
            infolist = json.loads(java)['searchPageProps']['searchMapProps']['mapState']['markers']
            for i in range(0,len(infolist)-2):
                url = "https://www.yelp.com" + infolist[i]["url"]
                import ipdb; ipdb.set_trace()
                yield {
                    "url" : url,
                    "lat" : infolist[i]["location"]["latitude"],
                    "lon" : infolist[i]["location"]["longitude"]
                }



        except:
            reviews = json.loads(javascript.getall()[-1].strip('<script type="application/ld+json">').strip('\n'))["review"]
            for i in range(len(reviews)):
                rating_val = reviews[i]["reviewRating"]["ratingValue"]
                date = reviews[i]["datePublished"]

            # import ipdb; ipdb.set_trace()
            print("error")
             

