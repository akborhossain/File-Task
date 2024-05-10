from django import views
from django.urls import path
from .views import *


urlpatterns=[

    path('file_up/',DocUploadedView.as_view()),
    path('file_up/<int:pk>',DocUploadedView.as_view()),
    path('public_view/',DocFilePublicView.as_view()),
    path('public_view/<int:pk>',DocFilePublicView.as_view()),
    path('login/', LogedInView.as_view()),
    path('signup/', UserRegistrationAPIView.as_view()),
    path('status_change/<int:pk>',UserStatusView.as_view()),

]