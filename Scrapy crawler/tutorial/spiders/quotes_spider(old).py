import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = []
        baseUrl = 'http://allrecipes.com/recipe/'


        for index in range(14745,14765):
            urls.append(baseUrl+str(index))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        if response.xpath('//link[@rel="amphtml"]'):
            ingredientList = []
            directionList = []

            for sel in response.xpath('//ul/li/label/span[@class="recipe-ingred_txt added"]/text()'):
                test = sel.extract()
                ingredientList.append(test)
                #print(ingredientList)

            time = response.xpath('//span[@class="ready-in-time"]/text()').extract_first()
            #print(time)

            servings = response.xpath('//meta[@id="metaRecipeServings"]/@content').extract_first()
            #print(servings)

            title = response.xpath('//meta[@property="og:title"]/@content').extract_first()

            for sel in response.xpath('//span[@class="recipe-directions__list--item"]/text()'):
                    direction = sel.extract()
                    directionList.append(direction)
            #print(directionList)
            rating = response.xpath('//meta[@property="og:rating"]/@content').extract_first()

            #number_of_raters = response.xpath('//div[@class=total-made-it]/@data-ng-init').extract_first()
            #print(number_of_raters)

            category = response.xpath('//span[@class="toggle-similar__title"]/text()').extract()
            for index in range(len(category)):
                category[index] = category[index].strip()

            category = category[2:]

            special_key = response.xpath("//script[re:test(text(),'var RdpInferredTastePrefs =','i')]").extract()
            #start = special_key[0].find("[")
            #end = special_key[0].find("]")
            #keys = special_key[0][start+2:end-1]

            #re.sub(r'\W+', '', keys)


            #print(keys)
            #final_key = []
            #final_key.append(keys)

            #for index in range(len(final_key)):
            #    category.append(final_key[index])

            print(category)
            dic = {'ingredients': ingredientList, 'time': time, 'servings': servings , 'directions' : directionList , 'title' : title, 'rating' : rating, 'category': '', 'unit': 'US', 'clicks': "1", 'author': 'allrecipes', 'comments': '',
                   'relevance': '', 'pictures': ''}


            dic = split_that_dic(dic)
            #print(dic)
            yield dic


def split_that_dic(dic):
    splitted_dic = {}
    list_of_ing = []
    split_words = ["package", "packages", "can", "cans", "jar", "jars", "pound", "pounds", "cup", "cups", "teaspoon",
                   "teaspoons", "stalks", "stalk", "dash", "inch)", "ounce", "ounces"
                                                                             "fluid ounces", "fluid ounce", "envelope",
                   "envelopes", "bunch", "slice", "slices", "1", "2", "3", "4", "5", "6", "7", "8", "9", "tablespoon",
                   "tablespoons", "bottle", "quart", "pound)"]
    ingredients = dic.get('ingredients')
    # print(ingredients)


    for index in range(len(ingredients)):
        split = ingredients[index].split()
        ingredients[index] = split

    for elements in ingredients:
        for index in reversed(range(len(elements))):
            if elements[index] in split_words:
                splitted_dic["type"] = " ".join(elements[index + 1:])
                splitted_dic["amount"] = " ".join(elements[0:index + 1])
                list_of_ing.append(splitted_dic)
                splitted_dic = {}
                break

    del dic["ingredients"]
    dic["ingredients"] = list_of_ing
    # print(ingredients)
    # print(splitted_dic)

    return dic