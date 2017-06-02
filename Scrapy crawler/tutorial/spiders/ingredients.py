import scrapy


class IngredientSpider(scrapy.Spider):
    name = "ingredients"

    def start_requests(self):
        urlList=[]
        baseUrl = "http://www.bbc.co.uk/food/ingredients/by/letter/"
        letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        letter_list1 = ["a"]
        for index in range(len(letter_list)):
            urlList.append(baseUrl+letter_list[index])

        for url in urlList:
            yield scrapy.Request(url=url, callback=self.parse)


    #def page_parse(self, response):
     #   baseUrl = "http://www.foodista.com"
    #    recipe_page = response.xpath('//span[@class="field-content"]/a/@href').extract()



    #    for index in range(20):
    #        yield scrapy.Request(url=baseUrl+recipe_page[index], callback = self.parse)



    def parse(self, response):

        name = response.xpath('//ol[@class="resources foods grid-view"]/li/a/text()').extract()
        #prefixes = ("\n                        ")
        new_name_list = []
        for index in range(len(name)):
            name_striped=name[index].strip()
            #name[index] = name_striped
            if not(name_striped == "" or name_striped.startswith("Related")):

                new_name_list.append(name_striped)

        print(new_name_list)
        dictionary = {"ingredients": new_name_list}

        #while
        yield dictionary
