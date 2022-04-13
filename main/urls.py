# django stuff 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_home, name='redirect_home'), 

    path('home/<str:project_id>', views.home, name='home'),

    # project urls
    path('project-overall/<str:project_id>', views.project_overall, name='project_overall'),
    path('select-project/', views.select_project, name='select_project'),
    path('project-settings/<str:project_id>', views.project_settings, name='project_settings'),
    path('create-project/', views.create_project, name='create_project'),

    # others
    path('user-details/<str:username>', views.user_details, name='user_details'),
    path('view-all-comments/<str:project_id>', views.view_all_comments, name='view_all_comments'),
    path('view-all-timeline/<str:project_id>', views.view_all_timeline, name='view_all_timeline'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('chat/', views.chat, name='chat'),

    # POST managers
    path('comments-manager/<str:home>', views.new_comments_manager, name='new_comments_manager'),
    path('new-task-manager/', views.new_task_manager, name='new_task_manager'),
    path('complete-task/', views.set_task_as_completed, name='set_task_as_completed'),

    # APIs
    path('comments_api/', views.comments_api, name='comments_api'),
    path('timeline_api/', views.timeline_api, name='timeline_api'),
    path('send_message_api/', views.send_message_api, name='send_message_api'),
    path('get-users/', views.get_users_api, name='get_users_api'),
    ]