# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Place(scrapy.Item):
    url = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    searchActions = scrapy.Field()
    allPhotosHref = scrapy.Field()
    reviewCount = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    phone = scrapy.Field()
    allPhotosHref = scrapy.Field()
    photoHref = scrapy.Field()
    reviewCount = scrapy.Field()
    formattedAddress = scrapy.Field()
    categories = scrapy.Field()

class Review(scrapy.Item):
    ratingValue = scrapy.Field()
    datePublished = scrapy.Field()
    url = scrapy.Field()
    
