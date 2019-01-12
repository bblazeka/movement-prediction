from django.urls import path
from . import views
urlpatterns = [
    path('api/path/', views.PointListCreate.as_view() ),
    path('api/path/all/', views.AllPathsListCreate.as_view() ),
]