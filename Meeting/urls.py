from django.urls import path
from Meeting.views import signup, change_status, dashboard, login_func, create_meeting

app_name = 'Meeting'
urlpatterns = [
    path('signup/', signup, name='sign_up'),
    path('change_status/', change_status, name='change_status'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_func, name='login'),
    path('create_meeting/', create_meeting, name='create_meeting')
]
