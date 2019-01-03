from points.models import Point
from points.serializers import PointSerializer
from rest_framework import generics
from . import regression

class PointListCreate(generics.ListCreateAPIView):
    queryset = regression.regress([[-8.585,41.148],[-8.585,41.148],[-8.585,41.148],[-8.585,41.148]],"A",7)
    serializer_class = PointSerializer
