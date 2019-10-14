from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Drama, DramaSerializer
from .utils.crawler import update_drama


class DramaListCreateView(generics.ListAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('is_broadcasiting', 'broadcasting_day', 'broadcasting_start_time')

    def get(self, request, *args, **kwargs):
        update_drama()
        return Response()


class DramaRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
