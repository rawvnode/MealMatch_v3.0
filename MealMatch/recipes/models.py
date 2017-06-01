from mongoengine import *
from mongoengine import queryset_manager
import time
from django import forms
from .models import *
from collections import OrderedDict
from datetime import datetime
from django.contrib import admin


 ##### CUSTOM QUERYSETS #####
class mappedQuerysSet(QuerySet):  # Work similar to item_frequency and mapreduce. Maps count with keys

    def get_stats(keys):

        reduced_result = {}
        start = time.time()
        clicks_rating = recipe.objects.filter(id__in=keys).exclude('ingredients_list').exclude('directions')#Exclude speeds up the query process
        for item in clicks_rating:


            reduced_result[item.id] = {"clicks": item.clicks, "rating": item.ratings, "title": item.title, "ing_count": len(item.ingredients_complete), "image": item.image}

        end = time.time()

        return reduced_result

    def join(reduced_result, freq):
        for item in reduced_result:
            reduced_result[item]["frequency"] = freq[item]
            reduced_result[item]["ratio"] = int(100*freq[item]/reduced_result[item].get('ing_count'))




        return reduced_result

    def key_frequency(self, q1): #maybe to be renamed
        freq = self.item_frequencies("value") ##key frequency
        freq = OrderedDict(reversed(sorted(freq.items(),key=lambda x: (x[1])))) ##sorts by key frequency
        if q1 == []:
            query_keys = list(freq.keys())[0:1000]
        else:
            intersection = set(q1).intersection(list(freq.keys())) #does this preserve the order of things?
            #print(intersection)
            #relative_complement = set(q1).difference(list(freq.keys()))
            #print("rel compt ", relative_complement)
            #query_keys = intersection.update(relative_complement)


            query_keys = list(intersection)[0:1000]
        reduced_result = mappedQuerysSet.get_stats(query_keys)
        returnval = mappedQuerysSet.join(reduced_result, freq)
        return returnval

class ingredients(Document):
    amount = ListField(required=True)
    type = ListField(required=True)



class rating(EmbeddedDocument):
    user = IntField(required = True)
    rating = IntField()

    class Meta:
        fields = ['user' 'rating']




class Comment(EmbeddedDocument):
    created_at = DateTimeField(default = datetime.now, required=True)
    author = ObjectIdField(required=True)
    #email  = EmailField(verbose_name="Email")
    username = StringField(verbose_name="Username", max_length=255, required=True)
    body = StringField(verbose_name="Comment", required=True)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass


class recipe(DynamicDocument):
    title = StringField(required=True)
    time = StringField()
    servings = StringField()
    directions = ListField(required=True)
    ingredients_list = ListField()
    ingredients_complete = ListField()
    ratings = ListField(EmbeddedDocumentField('rating'))  # has to be 1 by default
    category = ListField()
    clicks = IntField(default=1)
    relevance = IntField()
    author = StringField(default='By MealMatch')
    comments = ListField(EmbeddedDocumentField('Comment'))
    pictures = StringField()
    #id = ObjectIdField(primary_key=True)

    meta = {'strict': False}  # What is this?

    @queryset_manager
    def objects(self, queryset): #sets default ordering when calling 'objects' on a collection

        return queryset.order_by("-clicks")

#class Recipes(models.Model):
        #user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

## mapped models ##
class mapped_id(Document):
    id = ObjectIdField(primary_key=True)


class mapped(Document):
    id = StringField(primary_key=True)
    value = ListField(ObjectIdField(primary_key=True))
    #value = ListField(EmbeddedDocumentField('mapped_id'))
    #value = DictField() <--- restore this to get working queryset
    title = StringField()
    meta = {'queryset_class': mappedQuerysSet}  # Defines a custom queryet

class food_ref(Document):
    foods = StringField(required=True)
    # _id = StringField(primary_key=True)

class autocorrect(Document):
    id = ObjectIdField(primary_key=True)
    food = StringField()






