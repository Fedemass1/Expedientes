from django.contrib.auth.views import LogoutView
from django.urls import path

from Accounts.views import login_request

urlpatterns = [
    path('login/', login_request, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
