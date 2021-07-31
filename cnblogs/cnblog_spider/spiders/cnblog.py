import scrapy
from cnblog_spider.items import CnblogSpiderItem
import datetime


class CnblogSpider(scrapy.Spider):
    name = 'cnblog'
    # allowed_domains = ['cnblog.com/sitemap/p']

    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            f'https://www.cnblogs.com/sitehome/p/{i}' for i in range(1, int(page) + 1)]

    def parse(self, response):
        item = CnblogSpiderItem()
        hrefs = response.xpath(
            "//div[@class='post-item-text']/a/@href").getall()
        titles = response.xpath(
            "//div[@class='post-item-text']/a/text()").getall()
        output = ''
        for (title, href) in zip(titles, hrefs):
            # print(href, title)
            output = title + '  ' + href
            item['string'] = output
            yield item

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time - start_time)
