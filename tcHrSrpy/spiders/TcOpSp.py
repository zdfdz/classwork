# -*- coding: utf-8 -*-
import scrapy
from tcHrSrpy.items import TchrsrpyItem


class TcopspSpider(scrapy.Spider):
    name = 'TcOpSp'
    allowed_domains = ['tencent.com']
    offset = 0
    url = "https://hr.tencent.com/position.php?&start="
    start_urls = [url + str(offset)]

    def parse(self, response):
        tcOp_list = response.xpath('//tr[@class = "even"] | //tr[@class = "odd"]')
        for each in tcOp_list:
            item = TchrsrpyItem()
            # 职位名称
            OpName = each.xpath("./td[1]/a/text()").extract()
            # 职位链接
            OpLink = each.xpath("./td[1]/a/@href").extract()
            # 职位类别
            OpType = each.xpath("./td[2]/text()").extract()
            # 职位人数
            OpNum = each.xpath("./td[3]/text()").extract()
            # 工作地点
            OpLocal = each.xpath("./td[4]/text()").extract()
            # 发布时间
            OpCommitTime = each.xpath("./td[5]/text()").extract()

            # 添加到集合中
            item['OpName'] = OpName[0]
            item['OpLink'] = OpLink[0]
            try:
                item['OpType'] = OpType[0]
            except:
                item['OpType'] = "0"
            item['OpNum'] = OpNum[0]
            item['OpLocal'] = OpLocal[0]
            item['OpCommitTime'] = OpCommitTime[0]
            yield item
        # 一页10个,offset+10为当前页的下一页
        if self.offset < 600:
            self.offset += 10
        # 重新回调self.parse
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
