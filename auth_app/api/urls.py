from django.urls import path, include
from .views import UserProfileList, UserProfileDetail, RegistrationView,\
    CustomLoginView, EmailCheckView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check')
]