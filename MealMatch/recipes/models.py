from mongoengine import *
from mongoengine import queryset_manager
import time
from .models import *
from collections import OrderedDict


 ##### CUSTOM QUERYSETS #####
class mappedQuerysSet(QuerySet):  # Work similar to item_frequency and mapreduce. Maps count with keys

    def get_stats(keys):

        reduced_result = {}
        start = time.time()
        clicks_rating = recipe.objects.filter(id__in=keys).exclude('ingredients_list').exclude('directions')#Exclude speeds up the query process
        for item in clicks_rating:
            #print(item.rating)
            reduced_result[item.id] = {"clicks": item.clicks, "rating": item.rating, "title": item.title, "ing_count": len(item.ingredients_complete), "image": item.image}
        end = time.time()
        print(end - start)
        return reduced_result

    def join(reduced_result, freq):
        for item in reduced_result:
            reduced_result[item]["frequency"] = freq[item]
            reduced_result[item]["ratio"] = int(100*freq[item]/reduced_result[item].get('ing_count'))




        return reduced_result

    def key_frequency(self): #maybe to be renamed

        freq = self.item_frequencies("value") ##key frequency
        freq = OrderedDict(reversed(sorted(freq.items(),key=lambda x: (x[1])))) ##sorts by key frequency


        query_keys = list(freq.keys())[0:1000]


        reduced_result = mappedQuerysSet.get_stats(query_keys)

        returnval = mappedQuerysSet.join(reduced_result, freq)
        #print(type(returnval))
        return returnval






### Old (deleter after 26th of april):
 #arr = []
       #for item in self:
       #    for key in item.value:
       #        arr += list(key.to_mongo().to_dict().values()) #helt orimlig rad, jag vet. //Fabian

        #freq = {x: arr.count(x) for x in arr}
## recipe models ##

class ingredients(Document):
    amount = ListField(required=True)
    type = ListField(required=True)

class rating(Document):
    user_rated = StringField(required=True)
    recipe_rating = DecimalField(default=1, min_value=1, max_value=5, precision=4)

class comments(Document):
    username = StringField()
    user_comment = StringField()




class recipe(DynamicDocument):
    title = StringField(required=True)
    time = StringField()
    servings = IntField()
    directions = ListField(required=True)
    ingredients_list = ListField()
    ingredients_complete = ListField()
    rating = ListField(EmbeddedDocumentField('rating'))  # has to be 1 by default
    category = ListField(required=True)
    clicks = IntField(required=True, default=1)
    relevance = IntField()
    author = StringField(default='By MealMatch')
    comments = ListField(EmbeddedDocumentField('comments'))
    pictures = StringField()
    #id = ObjectIdField(primary_key=True)

    meta = {'strict': False}  # What is this?

    @queryset_manager
    def objects(self, queryset): #sets default ordering when calling 'objects' on a collection
        print("ordering")
        return queryset.order_by("-clicks")


## mapped models ##
class mapped_id(Document):
    id = ObjectIdField(primary_key=True)

class mapped(Document):
    value = ListField(ObjectIdField(primary_key=True))
    #value = ListField(EmbeddedDocumentField('mapped_id'))
    #value = DictField() <--- restore this to get working queryset
    meta = {'queryset_class': mappedQuerysSet}  # Defines a custom queryet

class food_ref(Document):
    food = StringField(required=True)
    # _id = StringField(primary_key=True)





