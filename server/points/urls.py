from django.urls import path
from . import views
urlpatterns = [
    path('api/point/', views.PointListCreate.as_view() ),
]