import json
import scrapy

URL = "https://www.yelp.com/search?find_desc=&find_loc=tucson&ns=1&start={page}"

class YelpSpider(scrapy.Spider):
    name = "yelp"
    start_urls = [URL.format(page=i) for i in range(0,1000,10)]

    def parse(self, response):
        try: 
            javascript = response.css('script::text').getall()
            java = javascript[12].strip("<!--").strip("-->")
            infolist = json.loads(java)['searchPageProps']['searchMapProps']['mapState']['markers']
            for i in range(0,len(infoilst)-2):
                yield {
                    "url" : "https://www.yelp.com" + infolist[i]["url"],
                    "lat" : infolist[i]["location"]["latitude"],
                    "lon" : infolist[i]["location"]["longitude"],
                }

        except:
            import ipdb; ipdb.set_trace()
             

