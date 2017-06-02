

def split_that_dic(dic):
    splitted_dic = {}
    list_of_ing = []
    split_words = ["package", "packages", "can", "cans", "jar", "jars", "pound", "pounds", "cup", "cups", "teaspoon", "teaspoons", "stalks", "stalk", "dash", "inch)", "ounce", "ounces"
                   "fluid ounces", "fluid ounce", "envelope", "envelopes", "bunch", "slice", "slices", "1", "2", "3", "4", "5", "6", "7", "8", "9", "tablespoon", "tablespoons", "bottle", "quart", "pound)"]
    ingredients = dic.get('ingredients')
    #print(ingredients)


    for index in range(len(ingredients)):
        split = ingredients[index].split()
        ingredients[index] = split


    for elements in ingredients:
        for index in reversed(range(len(elements))):
            if elements[index] in split_words:
                splitted_dic["type"] = " ".join(elements[index+1:])
                splitted_dic["amount"] =  " ".join(elements[0:index+1])
                list_of_ing.append(splitted_dic)
                splitted_dic = {}
                break



    del dic["ingredients"]
    dic["ingredients"] = list_of_ing
    #print(ingredients)
    #print(splitted_dic)

    return dic



dic = {'servings': ['15'], 'directions': ['Preheat oven to 325 degrees F (165 degrees C).', 'Score ham, and stud with the whole cloves. Place ham in foil lined pan.', 'In the top half of a double boiler, heat the corn syrup, honey and butter. Keep glaze warm while baking ham.', 'Brush glaze over ham, and bake for 1 hour and 15 minutes in the preheated oven. Baste ham every 10 to 15 minutes with the honey glaze. During the last 4 to 5 minutes of baking, turn on broiler to caramelize the glaze. Remove from oven, and let sit a few minutes before serving.'], 'ingredients': ['1 (5 pound) ready-to-eat ham', '1/4 cup whole cloves', '1/4 cup dark corn syrup', '2 cups honey', '2/3 cup butter'], 'time': ['1 h 35 m'], 'title': ['Honey Glazed Ham Recipe']}

split_that_dic(dic)




