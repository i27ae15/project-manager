import uuid
import pymongo

from django.shortcuts import render, redirect
from .forms import RegisterForm


# connecting to the data base ---------------------------------------------------
# ONLINE_CLIENT = pymongo.MongoClient("mongodb+srv://userTestOne:aM2ex0Wde9Hy7C7v@cluster0.m226z.mongodb.net/sample_restaurants?retryWrites=true&w=majority", tlsCAFile=ca)

LOCAL_CLIENT = pymongo.MongoClient()

# First define the database name

db_name = LOCAL_CLIENT['ProjectManager']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
# ------------------------------------------------------------------------------

# Constants

MANAGER_LEVEL = 1

# independents collections
PROJECTS_COLLECTION = db_name['projects']
USER_COLLECTION = db_name['auth_user']
USER_INFO_COLLECTION = db_name['user_info']

def create_user_info(user):

    user_info = {
        'id':user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'username': user['username'],
        'email': user['email'],
        'profile_photo': '',
        'role': '',
        'current_task': '',
        'city': '',
        'country': '',
        'phone': '',
        'about_me': '',
        'current_project': '',
        'chats': [],
        'comments': [],
        'notifications': [], 
        'user_level': 0,  
    }

    USER_INFO_COLLECTION.insert_one(user_info)

      

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

        username = form.cleaned_data['username']
        user = USER_COLLECTION.find_one({'username': username})
        create_user_info(user)
        return redirect('select_project')
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {'form':form})