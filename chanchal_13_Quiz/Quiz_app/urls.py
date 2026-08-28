from django.urls import path
from Quiz_app.quiz_views import *
from Quiz_app.views import *

urlpatterns = [
    path('home/', home_view, name='home_view'),
    path('register/', register_view, name='register_view'),
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    

    path('profile/', profile_view, name='profile_view'),
    path('profile_update/', profile_update_view, name='profile_update_view'),


    path('quiz_list/', quiz_list_view, name='quiz_list_view'),
    path('quiz_create/', quiz_create_view, name='quiz_create_view'),
    path('quiz_edit/<str:quiz_id>/', quiz_edit_view, name='quiz_edit_view'),
    path('quiz_delete/<str:quiz_id>/', quiz_delete_view, name='quiz_delete_view'),


    path('question_list/<str:quiz_id>/', question_list_view, name='question_list_view'),
    path('question_add/<str:quiz_id>/', question_add_view, name='question_add_view'),
    path('question_update/<str:question_id>/', question_edit_view, name='question_edit_view'),
    path('question_delete/<str:question_id>/', question_delete_view, name='question_delete_view'),


    path('option_list_view/<str:question_id>/', option_list_view, name='option_list_view'),
    path('option_add/<str:question_id>/', option_add_view, name='option_add_view'),
    path('option_update/<str:option_id>/', option_edit_view, name='option_edit_view'),
    path('option_delete/<str:option_id>/', option_delete_view, name='option_delete_view'),


    path('take_quiz/<str:quiz_id>', take_quiz_view, name='take_quiz_view'),
    path('quiz_result/<str:quiz_id>', quiz_result_view, name='quiz_result_view'),
    path('quiz_attempt/', quiz_attempt_view, name='quiz_attempt_view'),
]
