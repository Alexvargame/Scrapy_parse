from scrapy.selector import Selector

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Spider
from wikiSpider.items import Article

class ArticleSpider(Spider):
    name='article'
    allowed_domains=['en.wikipedia.org']
    start_urls=['http://en.wikipedia.org/wiki/Main_Page']
    rules=[Rule(LinkExtractor(allow=('(/wiki/)((?!:).)*$'),),callback='parse_items',follow=True)]

    

    def parse_items(self,response):
        print('WWWWWWWWWWWWWWWWWWWWWWWW')
        item=Article()
        print(item)
        title=response.xpath('//h1/text()')[0].extract()
        print("Title is:"+title)
        item['title']=title
        return item

    
