from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Drama, DramaSerializer
from datetime import datetime


class DramaListCreateView(generics.ListAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer

    # 필드로 필터링할 때 사용하는데 on-air 인지 아닌지만 판단하기때문에 필드로 판단 불가해서 사용하지 않을듯
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_broadcasiting',)

    def get(self, request, *args, **kwargs):
        query_params = request.query_params.get('onair')
        if query_params == 'true':
            days_of_week = ['월', '화', '수', '목', '금', '토', '일']
            queryset = Drama.objects.filter(is_broadcasiting=True,
                                            broadcasting_day__name__in=[days_of_week[datetime.today().weekday()]],
                                            broadcasting_start_time__lte=datetime.now(),
                                            broadcasting_end_time__gte=datetime.now()).prefetch_related(
                'broadcasting_day').prefetch_related('genre')
        else:
            queryset = Drama.objects.filter(is_broadcasiting=True).prefetch_related(
                'broadcasting_day').prefetch_related('genre')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
