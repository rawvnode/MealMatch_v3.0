from mongoengine import *


# Create your models here.
class ingredients(Document):
    amount = ListField(required=True)
    type = ListField(required=True)

class rating(Document):
    user_rated = StringField(required=True)
    recipe_rating = DecimalField(default = 1, min_value = 1, max_value = 5, precision = 4)

class comments(Document):
    username = StringField()
    user_comment = StringField()


class recipe(DynamicDocument):
    title = StringField(required=True)
    time = StringField()
    servings = IntField()
    directions = ListField(required=True)
    ingredients = ListField(EmbeddedDocumentField('ingredients'))
    rating = ListField(EmbeddedDocumentField('rating'))  # has to be 1 by default
    category = ListField(required=True)
    clicks = IntField(required=True, default = 1)
    relevance = IntField()
    author = StringField(default = 'By MealMatch')
    comments = ListField(EmbeddedDocumentField('comments'))
    pictures = StringField()


    meta = {'strict' : False}

class food(Document):
    food = StringField(required=True)
    group = StringField(required=True)
    subgroup = StringField(required=True)
