import scrapy
import re
from phonedb.items import ModelItem


class PhoneSpider(scrapy.Spider):
    name = "pspider"
    allowed_domains = ["gsmarena.com"]
    start_urls = [
        "http://www.gsmarena.com/makers.php3"
    ]

    tag_re = re.compile(r'<[^>]+>', re.S)

    def parse(self, response):
        # url = 'http://www.gsmarena.com/acer_liquid_z6_plus-8305.php'
        # yield scrapy.Request(url, callback=self.parse_detail_info)

        for sel in response.xpath('//div[@class="st-text"]/table/tr[*]/td[*]'):
            href = sel.xpath('a/@href')
            url = response.urljoin(href.extract()[0])

            """
            temp = sel.extract().replace('<br>', '|')
            result = PhoneSpider.tag_re.sub('', temp).split('|')
            #print result[0], result[1], response.urljoin(href.extract()[0])
            item = BrandItem()
            item['name'] = result[0]
            item['count'] = result[1]
            item['url'] = url
            """
            yield scrapy.Request(url, callback=self.parse_model)

    def parse_model(self, response):
        #title = response.xpath('//title/text()').extract()[0]
        for sel in response.xpath('//*[@id="review-body"]/div/ul/li[*]'):
            """
            example result:
            '<li><a href="acer_iconia_talk_s-8306.php">' \
            '<img src="http://cdn2.gsmarena.com/vv/bigpic/acer-iconia-talk-s.jpg" ' \
            'title="Acer Iconia Talk S Android tablet. Announced 2016, August. Features 3G, 7.0\u2033 IPS LCD capacitive touchscreen, 13 MP camera, Wi-Fi, GPS, Bluetooth.">' \
            '<strong><span>Iconia Talk S</span></strong></a></li>'
            """

            href = sel.xpath('a/@href')
            url = response.urljoin(href.extract()[0])
            yield scrapy.Request(url, callback=self.parse_detail_info)

    def parse_detail_info(self, response):
        # desc = response.xpath('//meta[2]').extract()[0].split('"')[3]
        """
        desc xpath content example:
        '<meta name="Description" content="Acer Liquid Z6 Plus Android smartphone. ' \
       'Announced 2016, August. Features 5.5\u2033 IPS LCD capacitive touchscreen, ' \
       '13 MP camera, Wi-Fi, GPS, Bluetooth.">'
        """
        item = ModelItem()
        item_class = {}
        name = response.xpath('//*[@id="body"]/div/div[1]/div/div[1]/h1/text()').extract()[0]
        for sel in response.xpath('//*[@id="specs-list"]/table[*]'):
            item_key = sel.xpath('tr[1]/th/text()').extract()[0]
            item_dict = {}
            for tup in sel.xpath('tr[*]'):
                key_list = tup.xpath('td[1]/a/text()').extract()
                attr = tup.xpath('td[2]').extract()[0]
                attr = PhoneSpider.tag_re.sub('', attr)
                """
                do so because sometimes the tag will be for example:
                '<td class="nfo"><a href="#" class="link-network-detail collapse">GSM / HSPA / LTE</a></td>'
                rather than
                '<td class="nfo"> HSDPA</td>'
                use td[2]/text() will return a null list
                """
                if len(key_list) == 0:
                    key = "null_key"
                else:
                    key = key_list[0]

                key = key.replace(u'\xa0', '')
                attr = attr.replace(u'\xa0', '')
                if key == "":
                    key = "null_key"
                item_dict[key] = attr
            item_class[item_key] = item_dict

        item['content'] = item_class
        item['name'] = name
        item['url'] = response.url
        item['image_urls'] = response.xpath('//*[@id="body"]/div/div[1]/div/div[2]/div/a/img/@src').extract()[0]
        yield item






