# django stuff 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project-overall/', views.project_overall, name='project_overall'),
    path('user-details/<str:username>', views.user_details, name='user_details'),
    path('view-all-comments/', views.view_all_comments, name='view_all_comments'),
    path('view-all-timeline/', views.view_all_timeline, name='view_all_timeline'),
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
    ]