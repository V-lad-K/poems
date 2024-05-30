from django.urls import path

from .views import home
from .views import poem_detail
from .views import poem_create

app_name = 'poems'

urlpatterns = [
    path("home/", home, name="home"),
    path("create/", poem_create, name="poem_create"),
    path("<str:pk>/", poem_detail, name="poem_detail"),
]
