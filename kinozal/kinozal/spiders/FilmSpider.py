from scrapy.selector import Selector

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Spider
from ..items import Film

class FilmSpider(Spider):
    name='film'
    allowed_domains=['kinozal.tv']
    start_urls=['https://kinozal.tv/details.php?id=1104806']
    print('RRRRRRRRRRRRRRRRRRRRRRRRRRRRR',start_urls)
##    rules=[Rule(LinkExtractor(allow=('(/details)'),),
##                callback='parse_item',follow=True)]
##    
##
#((?!:).)*$'),),    

    def parse(self,response):
        print('EEEEEEEEEEEEEEEEee')
        item=Film()
        print('WWWWWWWWWW',item)
        film=response.xpath('//h1/text()')[0].extract()
        print("Film is:"+film)
        item['film']=film
        return item

    
