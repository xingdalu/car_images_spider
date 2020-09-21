# -*- coding: utf-8 -*-
import scrapy
from ..items import QicheItem


class QicheSpiderSpider(scrapy.Spider):
    name = 'qiche_spider'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/153.html#pvareaid=3454438']

    def parse(self, response):
        divs = response.xpath('//div[@class="uibox"]')[1::]
        for div in divs:
            title = div.xpath('.//div[@class="uibox-title"]//text()').get()
            urls = div.xpath('.//ul//li//img/@src').getall()
            image_urls = list(map(lambda x: response.urljoin(x), urls))
            item = QicheItem(title=title, image_urls=image_urls)
            yield item


