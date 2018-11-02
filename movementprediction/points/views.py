from points.models import Point
from points.serializers import PointSerializer
from rest_framework import generics
from . import regression

class PointListCreate(generics.ListCreateAPIView):
    queryset = regression.regress("41.15,-8.61,41.15,-8.61,41.15,-8.61","A")
    serializer_class = PointSerializer
