# python
import uuid
from datetime import datetime

# django 
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# mongo 
import pymongo
import certifi
from bson.objectid import ObjectId


# forms
from .forms import Comment, AnswerComment, NewActivity, PersonalDetails

# other imports
NOW = datetime.now()
ca = certifi.where()

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

project_tasks_collection = 'project_tasks'
comments_collection = 'comments'
timeline_collection = 'timeline'
chats_collection = 'chats'
messages_collection = 'messages'
user_tasks_collection = 'user_tasks'

PROJECT_TASKS_COLLECTION = db_name[project_tasks_collection]
COMMENTS_COLLECTION = db_name[comments_collection]
TIMELINE_COLLECTION = db_name[timeline_collection]
CHATS_COLLECTION = db_name[chats_collection]
MESSAGES_COLLECTION = db_name[chats_collection]
TASKS_COLLECTION = db_name[user_tasks_collection]


# TO DO -------------------------------------------------------------------------------------------
# to be able to post answer to comments
# -------------------------------------------------------------------------------------------------

# other functions ---------------------------------------------------------------------------------
def convert_mongo_collection_to_dict(data:dict, include_object_id:bool):
    data = dict(data)
    data_converted = dict()

    for key in data.keys():
        current_term = data[key]

        if type(current_term) == ObjectId:
            
            if not include_object_id:
                continue
            
            current_term = str(current_term)
            
        data_converted[key] = current_term
    
    return data_converted


def get_boolean(value):

    if str(value).lower() in ['true', '1']:
        return True
    
    return False


def get_info_from_answer(dict_object):
    answer = None
    for d in dict_object:
        user = USER_COLLECTION.find_one({'_id':d['user_id']})
        answer = {
            'user':user,
            'answer': d['answer'],
            'date': d['date']
            }
    
    return answer


def get_recent_comments(project_id:str, limit=5, skip=0, order=-1, ):
    """
    
    RETURN A LIST OF THE LAST N COMMENTS IN CURRENT PROJECT
    
    """
    recent_comments = COMMENTS_COLLECTION.find({'project_id': project_id}).sort('date', order).limit(limit).skip(skip)
    comments = []

    for c in recent_comments:
        current_comment = {}
        current_comment['comment'] = c['comment']
        current_comment['date'] = c['date']

        user_in_comment = USER_COLLECTION.find_one({'id': c['user_id']})
        current_comment['username'] = user_in_comment['username']
        current_comment['user_profile_photo'] = USER_INFO_COLLECTION.find_one({'id': user_in_comment['id']})['profile_photo']
        current_comment['user_status'] = user_in_comment['is_active']
        current_comment['answers'] = get_info_from_answer(c['answers'])

        comments.append(current_comment)

    return comments


def get_recent_acitivities_in_timeline(project_id:str, limit=5, skip=0):
    return TIMELINE_COLLECTION.find({'project_id':project_id}).sort('date', -1).limit(limit).skip(skip)


def get_recent_chats(user_id, get_current_chat=False):
    user_info = USER_INFO_COLLECTION.find_one({'user_id':user_id})
    info = {}
    recents_chats = []
    current_chat = None
    info['recent_chats'] = recents_chats

    for chat in user_info['chats']:
        new_chat_info = {}
        user = USER_COLLECTION.find_one({'id':chat['user_id']})
        new_chat_info['username'] = user['username']
        new_chat_info['profile_photo'] = USER_INFO_COLLECTION.find_one({'user_id':chat['user_id']})['profile_photo']

        if user['is_active']:
            new_chat_info['status'] = 'Online'
        else:
            new_chat_info['status'] = user['last_login']

        recents_chats.append(new_chat_info)

        if get_current_chat and current_chat is None:
            info['current_chat'] = MESSAGES_COLLECTION.find({'chat_id': chat['chat_id']}).sort('date', 1).limit(30)

    return info


def get_users_in_project(project_id:str):
    return USER_INFO_COLLECTION.find({'current_project': project_id}).sort('first_name')


def get_project_objetives(project_id:str):
    return PROJECTS_COLLECTION.find_one({'id': project_id})['objectives']

# -------------------------------------------------------------------------------------------------
# root 
# -------------------------------------------------------------------------------------------------


def redirect_home(request):
    return redirect('select_project')

# Project management

@login_required(login_url='login')
def select_project(request):
    # TODO: Itereate the list of developers, if it matches with the current, them send it to the frontend
    projects = PROJECTS_COLLECTION.find()
    current_user = USER_INFO_COLLECTION.find_one({'id': request.user.id})
    return render(request, 'main/main_pages/select-project.html', {'projects': projects, 'current_user': current_user})


@login_required(login_url='login')
def create_project(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        
        objectives = []
        obj = 0

        date_format = '%Y-%m-%d'

        while request.POST.get(f'objectives[{obj}][objective]') is not None:
            sub_objectives = []
            sub_obj = 0
            while request.POST.get(f'objectives[{obj}][sub_objectives][{sub_obj}][sub_objective]') is not None:

                new_sub_obj = {
                    'id': str(uuid.uuid4()), 
                    'completed': False,
                    'developers_on_this': 0,
                    'extension': False,
                    'sub_objective': request.POST.get(f'objectives[{obj}][sub_objectives][{sub_obj}][sub_objective]'),
                    'deadline': datetime.strptime(request.POST.get(f'objectives[{obj}][sub_objectives][{sub_obj}][deadline]'), date_format),
                }

                sub_objectives.append(new_sub_obj)
                sub_obj += 1

            new_obj = {
                'id': str(uuid.uuid4()), 
                'objective': request.POST.get(f'objectives[{obj}][objective]'),
                'deadline': datetime.strptime(request.POST.get(f'objectives[{obj}][deadline]'), date_format),
                'completed': False,
                'developers_on_this': 0,
                'extension': False,
                'sub_objectives': sub_objectives,
            }
        
            obj += 1
            objectives.append(new_obj)

        developers = []
        dev = 0

        while request.POST.get(f'developers[{dev}][id]') is not None:

            query = {'id':int(request.POST.get(f'developers[{dev}][id]'))}
            developer_role = request.POST.get(f'developers[{dev}][role]')

            if developer_role != '':
                current_dev = USER_INFO_COLLECTION.find_one_and_update(query, 
                {'$set': {'role':developer_role + ' developer'}})

            else:
                current_dev = USER_INFO_COLLECTION.find_one(query)
            
            new_dev = {
                'id': current_dev['id'],
                'username': current_dev['username'],
                'role': current_dev['role']
            }

            developers.append(new_dev)
            dev += 1

        new_project = {
        'id': str(uuid.uuid4()),
        'name': request.POST.get('project_name'),
        'resume': request.POST.get('project_resume'),
        'created': NOW.now(),
        'completed': False,
        'deadline': datetime.strptime(request.POST.get('project_deadline'), date_format),
        'extension': False,
        'developers': developers,
        'objectives': objectives
        }

        PROJECTS_COLLECTION.insert_one(new_project)
        return JsonResponse({'project_id': new_project['id']})

    else:

        users = USER_INFO_COLLECTION.find()
        managers = USER_INFO_COLLECTION.find({'user_level': {'$gt': MANAGER_LEVEL - 1}})

        return render(request, 'main/main_pages/create-project.html', {'users': users, 'managers': managers})


@login_required(login_url='login')
def project_overall(request, project_id:str):
    users = get_users_in_project(project_id=project_id)
    project_objectives = get_project_objetives(project_id=project_id)
    

    # getting the task that are waiting for aproval
    current_user = USER_INFO_COLLECTION.find_one({'id': request.user.id})

    tasks_waiting_for_aproval = TASKS_COLLECTION.find({'waiting_for_aproval': True})
    tasks:list = []

    for task in tasks_waiting_for_aproval:
        user = USER_INFO_COLLECTION.find_one({'user_id': task['user_id']})
        
        tasks.append({'task':task, 'user':user})
    

    return render(request, 'main/main_pages/project-overall.html', {'users':users, 'tasks':tasks, 'current_user': current_user, 'project_objectives': project_objectives, 'project_id': project_id})


@login_required(login_url='login')
def project_settings(request, project_id:str):
    return render(request, 'main/main_pages/project-settings.html')

# -------------------------------------------------------------------------------------------------

# Others

@login_required(login_url='login')
def home(request, project_id:str):
    comments = get_recent_comments(project_id=project_id)
    timeline = get_recent_acitivities_in_timeline(project_id=project_id)
    users = get_users_in_project(project_id=project_id)

    # forms
    comment_form = Comment()
    answer_comment_form = AnswerComment()
    new_milestone_form = NewActivity()

    return render(request, 'main/main_pages/dashboard.html', 
    {'comments':comments, 
    'comment_form':comment_form,
    'timeline':timeline,
    'users':users,
    'project_id': project_id,
    # Forms ----------------------------------------
    'answer_comment_form': answer_comment_form,
    'new_milestone_form': new_milestone_form,
    })


@login_required(login_url='login')
def view_all_comments(request, project_id:str):
    comment_form = Comment()
    comments = get_recent_comments(10)

    return render(request, 'main/main_pages/view_all_comments.html', 
    {
        'comment_form':comment_form,
        'comments':comments,
    })


@login_required(login_url='login')
def view_all_timeline(request, project_id:str):
    timeline = TIMELINE_COLLECTION.find().sort('date', -1)
    return render(request, 'main/main_pages/view-all-timeline.html', {'timeline':timeline})


@login_required(login_url='login')
def profile(request, username):

    current_logged_user = USER_INFO_COLLECTION.find_one({'id': request.user.id})

    if username == 'my_profile' or username == request.user.username:

        other_info = USER_INFO_COLLECTION.find_one({'user_id':request.user.id})
        user_info = {'main':request.user, 'user_info':other_info}
        chats = []

        for chat in other_info['chats']:
            username = USER_COLLECTION.find_one({'id':chat['user_id']})['username']
            profile_photo = USER_INFO_COLLECTION.find_one({'user_id':chat['user_id']})['profile_photo']
            new_chat = {'username':username, 'profile_photo':profile_photo} 
            chats.append(new_chat)
        
        user_info['chats'] = chats

        own_profile = True

    else:

        user = USER_COLLECTION.find_one({'username':username})
        other_info = USER_INFO_COLLECTION.find_one({'user_id':user['id']})
        user_info = {'main':user, 'user_info':other_info}
        own_profile = False

    user_info['current_task'] = TASKS_COLLECTION.find_one({'id': request.user.id})

    if user_info['current_task'] is None:
        user_info['current_task'] = False

    return render(request, 'main/main_pages/profile.html', {'user_info':user_info, 'own_profile':own_profile, 'current_logged_user': current_logged_user})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = PersonalDetails(request.POST)
        
        if form.is_valid():

            query = {'user_id': request.user.id}
            new_values = { "$set": 
            { 'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'email':form.cleaned_data['email'] } 
            }

            USER_COLLECTION.update_one(query, new_values)

            query = {'id': request.user.id}
            new_values = { "$set": 
            { 'phone':form.cleaned_data['phone'],
                'about_me':form.cleaned_data['about_me'],
                'city':form.cleaned_data['city'],
                'country':form.cleaned_data['country'], 
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'email':form.cleaned_data['email'] 
                } 
            }

            USER_INFO_COLLECTION.update_one(query, new_values)
            return redirect('profile', username=request.user.username)
        
        else:
            HttpResponse('An erros has ocurred with the form, please retry again')



    user_info = USER_INFO_COLLECTION.find_one({'id': request.user.id})
    form = PersonalDetails(initial={
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email,
        'phone':user_info['phone'],
        'about_me':user_info['about_me'],
        'city':user_info['city'],
        'country':user_info['country'],
        })
    return render(request, 'main/main_pages/edit-profile.html', {'user_info':user_info, 'form':form})
    

@login_required(login_url='login')
def chat(request, username=False):
    if username:
        # TO DO: when a username is passed it means that the user wants to chat with that person,
        # so the chat section must open in that chat
        pass

    chats_info = get_recent_chats(user_id=request.user.id, get_current_chat=True)
    user_info = USER_INFO_COLLECTION.find_one({'id':request.user.id})

    return render(request, 'main/main_pages/chat.html', {'chats_info':chats_info, 'user_info':user_info})


@login_required(login_url='login')
def user_details(request, username):

    user = USER_COLLECTION.find_one({'username':username})
    other_info = USER_INFO_COLLECTION.find_one({'user_id':user['id']})
    user_info = {'main_info':user, 'other_info':other_info}

    if request.user.username == username:
        own_profile = True
    else:
        own_profile = False

    tasks = TASKS_COLLECTION.find({'user_id':user['id']}).sort('date', -1).limit(10)
    current_user = USER_INFO_COLLECTION.find_one({'id':request.user.id})

    return render(request, 'main/main_pages/user-details.html', {'user_info':user_info, 'tasks':tasks, 'own_profile':own_profile, 'current_user':current_user})


# ------------------------------------------------------------------
# APIs
# ------------------------------------------------------------------

def comments_api(request):
    if request.is_ajax and request.method == 'POST':
        comments = {'comments':get_recent_comments(limit=10, skip=int(request.POST.get('skip')))}
        return JsonResponse(comments)
    
    return HttpResponse('FORBIDDEN')


def timeline_api(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        new_activity_in_timeline = {
            'activity': request.POST.get('activity'),
            'date': NOW.now()
        }
        TIMELINE_COLLECTION.insert_one(new_activity_in_timeline)
        return JsonResponse({'status': 200})

    else:
        return HttpResponse('FORBIDDEN')


def send_message_api(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        new_message = {
            'chat_id': request.POST.get('chat_id'),
            'sent_by': int(request.POST.get('user_id')),
            'seen': False,
            'date': NOW.now(),
            'text':request.POST.get('text')
        }

        MESSAGES_COLLECTION.insert_one(new_message)
        return JsonResponse({'status': 200})
    else:
        return HttpResponse('FOBIDDEN')


def get_users_api(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':

        users_docs = USER_INFO_COLLECTION.find()
        users = []

        for user in users_docs:
            users.append(convert_mongo_collection_to_dict(data=user, include_object_id=False))

        return JsonResponse({'users':users})

    else:
        return HttpResponse('FOBIDDEN')

# ------------------------------------------------------------------
# POST MANAGERS
# ------------------------------------------------------------------

def new_comments_manager(request, home='True'):
    # we need the user that made the comment
    if 'submit_comment' in request.POST:
        form = Comment(request.POST)

        if form.is_valid():
            new_comment = {
                'id': str(uuid.uuid4()),
                'project_id': request.POST.get('project_id'),
                'user_id': request.user.id,
                'comment': form.cleaned_data['comment'],
                'date': NOW.now(),
                'answers': [],
            }

            query = {'id': request.user.id}
            new_values = { "$push": { "comments": new_comment['id']} }

            USER_INFO_COLLECTION.update_one(query, new_values)
            COMMENTS_COLLECTION.insert_one(new_comment)

    elif 'submit_answer':
        form = AnswerComment(request.POST)

        if form.is_valid():
            comment_to_answer = form.cleaned_data['comment']
            comment = COMMENTS_COLLECTION.find_one({'comment': comment_to_answer})

            new_answer = {
                '_id': ObjectId(),
                'user_id': comment['_id'],
                'answer': form.cleaned_data['answer'],
                'date': NOW
            }
            
            query = {'comment':comment_to_answer}
            new_values = {'$push': {'answers':new_answer}}
            COMMENTS_COLLECTION.update_one(query, new_values)

    if get_boolean(home):
        return redirect('home', project_id=request.POST.get('project_id'))
    else:
        return redirect('view_all_comments')


def new_task_manager(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        new_task = {
            'id': (uuid.uuid4()),
            'task': request.POST.get('task'),
            'details': request.POST.get('details'),
            'user_id': int(request.POST.get('user_id')),
            'date': NOW.now(),
            'deadline': request.POST.get('deadline'),
            'completed': False,
            'waiting_for_aproval': False,
            # HERE MUST BE CHANGE TO BE DYNAMIC
            'project': 'Project manager',
            'submited': NOW.now(),
        }

        TASKS_COLLECTION.insert_one(new_task)

        USER_INFO_COLLECTION.update_one(
            {'user_id': new_task['user_id']}, 
            {'$set': {'current_task': new_task['task']}})

        return JsonResponse({'status': 200})

    return HttpResponse('FORBIDDEN')
    

def set_task_as_completed(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':

        if request.POST.get('aprove') != 'None':

            aprove = get_boolean(request.POST.get('aprove'))

            current_task = TASKS_COLLECTION.find_one_and_update(
                {
                'id': (request.POST.get('task_id'))},
                {
                '$set': {'waiting_for_aproval': False, 'completed': aprove}}
                )
            
            user = USER_INFO_COLLECTION.find_one_and_update({'username': request.POST.get('username')}, 
            {'$set': {'working_on':''}})
            
            if aprove:
                msg = f'Your task "{current_task["task"]}" was aproved'
            else:
                msg = f'Your task "{current_task["task"]}" was not aproved'


            create_notification(user['_id'], 'Task revison', msg)
            return JsonResponse({'status': 200})

            
        
        current_task = TASKS_COLLECTION.find_one_and_update(
            {
            'id': (request.POST.get('task_id'))},
            {
            '$set': {'waiting_for_aproval': True}}
            )

        
        # send a notification for the person(s) in charge for revision of the task completed
        users = USER_INFO_COLLECTION.find({'current_project': current_task['project'] , 'user_level': {'$gt': 0}})
        

        for user in users:
            create_notification(
                user_id=ObjectId(user['_id']),
                notification_type='Task revision',
                message=f'New task for revison from {request.POST.get("username")}'
            )
        

        return JsonResponse({'status': 200})

    else:
        return HttpResponse('FORBIDDEN')


def create_notification(user_id:ObjectId, notification_type:str, message:str):
    """
    
    Create a notification and add it to the list/array of the user notifications

    Args:
        user_id (ObjectId): id of the user where the notification is added
        notification_type (str): the type of notification (message, task revision, other)
        message (str): a brief about the notification
    """

    new_notification = {
        'type': notification_type,
        'message': message,
        'id': str(uuid.uuid4())
        }

    USER_INFO_COLLECTION.find_one_and_update({'_id': user_id}, {'$push': {'notifications':new_notification}})