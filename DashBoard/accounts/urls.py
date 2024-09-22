from django.urls import path
from .views import SignUp, ConfirmUser

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('confirm/', ConfirmUser.as_view(), name='confirm'),
]