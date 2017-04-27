### Custom pipelines for the facebook login ###
import urllib.request
from .models import *



def user_profile(backend, details, response, uid, user, *args, **kwargs):

    #social_user.extra_data['access_token'],
    large_picture = 'http://graph.facebook.com/{0}/picture?type=large&access_token={1}'.format(response['id'], response['access_token'])
    data = 'https://graph.facebook.com/v2.9/{0}/?fields=gender,age_range,location,picture,name&access_token={1}'.format(response['id'], response['access_token'])
    gender = 'http://graph.facebook.com/{0}/age_range?&access_token={1}'.format(response['id'], response['access_token'])
    age =






    print('data:  ', data)
    #print(data.find('gender'))
    #profile = Profile(id = user.id, full_name = details['fullname'], first_name = details['first_name'], last_name = details['last_name'], facebook_id = uid, picture= large_picture, age= data.find('age_range'), sex = data.find('gender'))
    #return(profile.save())






