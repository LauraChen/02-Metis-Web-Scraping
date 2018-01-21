import scrapy
from selenium import webdriver



class cnSpider(scrapy.Spider):

    name = 'charity_nav'

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
            yield scrapy.Request(
                url=charity_links[i],
                callback=self.parse_charity,
                meta={'url': charity_links[i], 'name': charity_names[i]}
            )

    def parse_charity(self, response):
        
        name = response.request.meta['name']
        
        url = response.request.meta['url']


        state = (
            response.xpath('//div[@class="rating"]/p/text()').re(r'[A-Z]{2}')[0]
        )

        CEOsalary = (
            response.xpath('//td[@class="text-no-wrap"]/span/text()').extract()[0])

        perc_program_exp = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[0]
        )

        perc_admin_exp = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[1]
        )

        perc_fundraising_exp = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[2]
        )

        wking_cap_ratio = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[4]
        )

        program_exp_growth = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[5]
        )

        liab_to_assets = (
            response.xpath('//div[@class="accordion-item-bd"]/table/tr/td[@align="right"]/text()').extract()[6]
        )

        revenue = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[7]
        )

        admin_exp = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[12]
        )

        mkting_exp = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[13]
        )
        prog_rev = (
            response.xpath('//div[@class="accordion-item-bd rating"]/table/tr/td[@align="right"]/text()').extract()[9]
        )

        tpscore = (
            response.xpath('//div[@class="shadedtable"]/table/tr/td/text()').extract()[2]
        )

        yield {
            'url': url,
            'name': name,
            'state': state,
            'CEOsalary': CEOsalary,
            'revenue': revenue,
            'admin_exp': admin_exp,
            'mkting_exp': mkting_exp,
            'tpscore': tpscore,
            'perc_program_exp': perc_program_exp,
            'perc_admin_exp': perc_admin_exp,
            'perc_fundraising_exp': perc_fundraising_exp,
            'wking_cap_ratio':wking_cap_ratio,
            'program_exp_growth': program_exp_growth,
            'liab_to_assets': liab_to_assets

        }
