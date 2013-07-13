#TODO: wrap XPath selects that should result in only one node with verification
#TODO: consider verbose mode that outputs results of parsing steps even when parsing is as expected
#TODO: use proper logger
#TODO: turn url's and crawl steps into configuration
#TODO: use proper exception catching strategy
#TODO: unit test for every function
#TODO: system test against offline html copies

__author__ = 'matan'
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sys import exit

class MySpider(BaseSpider):
    name = 'www.o2.co.uk'
    allowed_domains = ['www.o2.co.uk']
    start_urls = [
        'https://www.o2.co.uk/shop/tariffs/#commitmentLengths=24+Months&monthlyCost=to_%C2%A320&minutes=from_50&texts=from_Unlimited&data=from_100MB&page=1'
    ]

    def parse(self, response):

        def spiderWarning(stage):
            self.log('Spider walk warning %s' % stage)

        def spiderBrokenExit(stage, details):
            self.log('Spider walk appears to be broken at %s. %s.' % (stage, details))
            exit() # to be refined

        self.log('Obtained response from %s' % response.url)
        self.log('Parsing starting')
        hxs = HtmlXPathSelector(response)
        plans = hxs.select('//tr[td[contains(@class, "monthlyCost")]]')

        if not plans:
            spiderBrokenExit(stage='locating plans on plans page', details='no plans located' )
        else:
            for plan in plans:
                #print plan.extract()

                monthlyCost = plan.select('td[contains(@class, "monthlyCost")]/text()').extract()
                print monthlyCost


                #link = site.select('a/@href').extract()
                #desc = site.select('text()').extract()
                #print title, link, desc
