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
        'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=24%20Months',
        'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=18%20Months'
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
                minutes = plan.select('td/span[contains(@class, "minsVal")]/text()').extract()
                messages = plan.select('td/span[contains(@class, "textsVal")]/text()').extract()
                data = plan.select('td/span[contains(@class, "dataAllowance")]/text()').extract()
                extras = plan.select('td/span[contains(@class, "extras")]/span/text()').extract()

                print monthlyCost + minutes + messages + data + extras

                #link = site.select('a/@href').extract()
                #desc = site.select('text()').extract()
                #print title, link, desc
