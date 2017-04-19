from mongoengine import *
from mongoengine import queryset_manager
import time
from .models import *
from collections import OrderedDict


 ##### CUSTOM QUERYSETS #####
class mappedQuerysSet(QuerySet):  # Work similar to item_frequency and mapreduce. Maps count with keys

    def get_stats(keys):
        limitval = 120 #The amount of results to query
        reduced_result = {}
        start = time.time()
        clicks_rating = recipe.objects.skip(len(keys) - limitval).filter(id__in=keys).exclude('ingredients_complete').exclude('directions')#Exclude speeds up the query process
        end = time.time()
        print(end - start)
        for item in clicks_rating:
            print(item.rating)
            reduced_result[item.id] = {"clicks": item.clicks, "rating": item.rating, "title": item.title, "ing_count": len(item.ingredients_list), "image": item.image}
        return reduced_result

    def join(reduced_result, freq):
        for item in reduced_result:
            reduced_result[item]["frequency"] = freq[item]
        return reduced_result

    def key_frequency(self): #maybe to be renamed
        freq = self.item_frequencies("value") ##key frequency
        freq = OrderedDict(reversed(sorted(freq.items(),key=lambda x: (x[1])))) ##sorts by key frequency
        print(freq)
        reduced_result = mappedQuerysSet.get_stats(freq.keys())

        returnval = mappedQuerysSet.join(reduced_result, freq)
        print(type(returnval))
        return returnval


    def get_related(self):
        reduced_result = mappedQuerysSet.get_stats(self.keys())
        return mappedQuerysSet.join(reduced_result, self)



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
    id = ObjectIdField(primary_key=True)

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





