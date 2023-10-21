import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        # count = response.xpath('//*[@id="example2"]/tbody/tr[1]/td[2]/a/text()').getall()
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            
            # absolute url
            # absolute_url = f'www.worldometers.info/{link}'

            # yield {
            # 'country_name' : country_name,
            # 'link' : link,
       
            #  }
            
            yield response.follow(url=link, callback = self.parse_country, meta= {'country': country_name})
    def parse_country(self, response):
        country = response.request.meta['country']
        rows= response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            # Return data extracted
            yield {
                'country':country,
                'year': year,
                'population':population,
            }