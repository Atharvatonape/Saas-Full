
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.profie_list_view),
    path('<username>/', views.profile_view)

]
