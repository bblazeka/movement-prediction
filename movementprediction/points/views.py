from points.models import Point
from points.serializers import PointSerializer
from rest_framework import generics

class PointListCreate(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    print(len(queryset))
    serializer_class = PointSerializer
