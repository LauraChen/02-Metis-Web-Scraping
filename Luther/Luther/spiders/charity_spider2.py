import scrapy



class cnSpider(scrapy.Spider):

    name = 'charity_nav2'

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.charitynavigator.org/index.cfm?FromRec=%s&bay=search.results&cgid=1&cuid=2' % page for page in range(0,321,20)
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        charity_links = response.xpath('//*[@id="searchresults"]/table/tbody/tr/td/div/h3/a/@href').extract()
        charity_names = response.xpath('//*[@id="searchresults"]/table/tbody/tr/td/div/h3/a/text()').extract()
        

        for i in range(len(charity_links)):
            data ={}
            data['url']=charity_links[i]
            data['name']=charity_names[i]
            yield scrapy.Request(
                url=charity_links[i],
                callback=self.parse_charity,
                meta={'data': data}
            )

    def parse_charity(self, response):
        
        data = response.meta['data']
        
        data ['state'] = (
            response.xpath('//div[@class="rating"]/p/text()').re(r'([A-Z]{2})\s\d+')[0]
        )

        data ['CEOsalary'] = (
            response.xpath('//td[@class="text-no-wrap"]/span/text()').re(r'[$|,|\d]+')[0]
        )

        data ['perc_program_exp'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[0]
        )

        data ['perc_admin_exp'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[1]
        )

        data ['perc_fundraising_exp'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[2]
        )

        data ['wking_cap_ratio'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[4]
        )

        data ['program_exp_growth'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[5]
        )

        data ['liab_to_assets'] = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[6]
        )

        data ['revenue'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[7]
        )

        data ['admin_exp'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[12]
        )

        data ['mkting_exp'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[13]
        )
        data ['prog_rev'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[9]
        )

        data ['tpscore'] = (
            response.xpath('//div[@class="shadedtable"]/table/tr/td/text()').extract()[2]
        )

        data ['gov_grant'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[6]
        )

        data ['service_rev'] = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[8]
        )

        yield scrapy.Request(
            url='https://www.charitynavigator.org/'+response.xpath('//li[@class="tabs-anchor"]/a/@href').extract()[2],
            callback=self.parse_IRSinfo,
            meta={'data': data}
            )

    def parse_IRSinfo(self, response):
        data=response.meta['data']
        data ['yr_founded'] = (
            response.xpath('//div[@class="shadedtable"]/table/tr/td/text()').re(r'[\w]+[,|\s]+([\d]{4})')[0]
        )

        yield data


