import scrapy


class IngredientSpider(scrapy.Spider):
    name = "foodista_ingredients"

    def start_requests(self):
        urlList=[]
        baseUrl = "http://www.foodista.com/browse/foods?page="


        for index in range(51):
            urlList.append(baseUrl+str(index))

        for url in urlList:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        name = response.xpath('//div[@class="view-content"]/div/div/span[@class="field-content"]/a/text()').extract()
        dictionary = {"ingredients": name}

        yield dictionary
