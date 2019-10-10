from rest_framework import generics
from .models import Drama, DramaSerializer


class DramaListCreateView(generics.ListCreateAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer


class DramaRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
