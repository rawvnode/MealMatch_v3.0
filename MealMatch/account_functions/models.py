from mongoengine import *
import mongoengine
import datetime
from django.db import models

# Create your models here.
#class comments(Document):
 #   recipe_id = StringField(required=True)
  #  user_comment = StringField(required=True)

class Profile(DynamicDocument):
    id = ObjectIdField(primary_key=True)
    mail = EmailField(required=True)
    favorites = ListField()
    my_recipies = ListField()
    #comments = ListField(EmbeddedDocumentField('comments'))
    picture = StringField() #facebook link
    my_info = StringField()
    sex = StringField()
    Pantry = ListField(default= ['Salt', 'Sea salt', 'Pepper','White pepper', 'Vinegar', 'Flour', 'Oil', 'Sugar', 'Pasta', 'Baking powder', 'Soy sauce', 'Broth', 'Honey', 'Tomato purée', 'Cinnamon', 'Oregano', 'Curry'])



