# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import ProductItem
from scrapy.linkextractors import LinkExtractor

class EastmoneySpider(CrawlSpider):
    name = "eastmoney"
    allowed_domains = ["eastmoney.com"]

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
       # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('http.*jbgk_\d{1,8}\.html', )), callback='parse_item'),
    )
    def __init__(self, productId=None, *args, **kwargs):
        super(EastmoneySpider,self).__init__(*args,**kwargs)
	#self.item = ProductItem()
	#self.item['seccode'] = productId
	self.start_urls = []
        #self.start_urls = ['http://fund.eastmoney.com/%s.html?spm=search' % productId]
	for value in productId.split(','):
	    self.start_urls.append('http://fund.eastmoney.com/%s.html?spm=search' % value)
	

    def parse_item(self,response):
	item = ProductItem()
	m = re.match(r'.*/jbgk_(\d{1,8})\.html.*', response.url)
	manageFee = re.match(r'.*(\d+\.\d+)%.*',response.xpath('//table//tr[7]/td[1]').extract()[0])
	trustFee = re.match(r'.*(\d+\.\d+)%.*',response.xpath('//table//tr[7]/td[2]').extract()[0])
	item['seccode'] = m.group(1) 
	item['manageFee'] = manageFee.group(1) 
	item['trustFee'] = trustFee.group(1)
#	self.item['completed'] = True
	return item


    def parse_start_url(self, response):
	item = ProductItem()
	m = re.match(r'.*/(\d{1,8})\.html.*', response.url)
	item['seccode'] = m.group(1) 
        item['unitnv'] = response.xpath('//dl[@class="dataItem02"]/dd[1]/span[1]/text()').extract()[0]
        item['accumulatedUnitnv'] = response.xpath('//dl[@class="dataItem03"]/dd[1]/span[1]/text()').extract()[0]
	return item
