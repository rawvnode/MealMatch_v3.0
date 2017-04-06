from mongoengine import *
import mongoengine
import datetime
from django.db import models

# Create your models here.
class comments(Document):
    recipe_id = StringField(required=True)
    user_comment = StringField(required=True)

class users(DynamicDocument):
    user_name = StringField(required=True)
    password = StringField(required=True)
    mail = EmailField(required=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    last_login = DateTimeField(default = datetime.datetime.now)
    favorites = ListField()
    my_recipies = ListField()
    comments = ListField(EmbeddedDocumentField('comments'))
    picture = StringField()
    my_info = StringField()



