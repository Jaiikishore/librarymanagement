from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name="home"),
    path('home', views.homepage, name="home"),
    path("viewbooks", views.show, name="show"),
    path("requestreservations", views.request_res, name="req"),
    path("cancelreservations", views.cancel_res, name="canc"),
]