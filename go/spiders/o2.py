#TODO: wrap XPath selects that should result in only one node with verification (& confirm no performance impact)
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
from scrapy.http import FormRequest
from sys import exit


class MySpider(BaseSpider):
    name = 'www.o2.co.uk'
    allowed_domains = ['www.o2.co.uk']
    start_urls = [
        'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=24%20Months'
        #'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=18%20Months'
    ]

    def parse_phones(self, response):

        '''
        phone details handler
        '''

        self.log('Parsing phoness....')

        hxs = HtmlXPathSelector(response)
        phones = hxs.select('//ul[@id="handsetList"]/li')
        print len(phones)

        if not phones:
            spider_broken_exit(stage='locating phones on phones page', details='no phones located' )
        else:
            for phone in phones:
                brand = phone.select('.//span[contains(@class, "brand")]/text()').extract()
                model = phone.select('.//span[contains(@class, "model")]/text()').extract()
                picture_url = phone.select('.//a/img/@src').extract()

                print brand + model + picture_url

    def parse(self, response):

        '''
        plans page handler
        '''

        def spider_warning(stage):
            self.log('Spider walk warning %s' % stage)

        def spider_broken_exit(stage, details):
            self.log('Spider walk appears to be broken at %s. %s.' % (stage, details))
            exit() # to be refined

        self.log('Obtained response from %s' % response.url)
        self.log('Parsing plans....')
        hxs = HtmlXPathSelector(response)
        plans = hxs.select('//tr[td[contains(@class, "monthlyCost")]]')

        if not plans:
            spider_broken_exit(stage='locating plans on plans page', details='no plans located' )
        else:
            for plan in plans:
                #print plan.extract()

                monthlyCost = plan.select('td[contains(@class, "monthlyCost")]/text()').extract()
                minutes = plan.select('td/span[contains(@class, "minsVal")]/text()').extract()
                messages = plan.select('td/span[contains(@class, "textsVal")]/text()').extract()
                data = plan.select('td/span[contains(@class, "dataAllowance")]/text()').extract()
                extras = plan.select('td/span[contains(@class, "extras")]/span/text()').extract()

                print monthlyCost + minutes + messages + data + extras

                return [FormRequest(url="https://www.o2.co.uk/shop/phones/",
                                                             callback=self.parse_phones)]

                #link = site.select('a/@href').extract()
                #desc = site.select('text()').extract()
                #print title, link, desc

