from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Drama, DramaSerializer, DramaEachEpisode, DramaEachEpisodeSerializer
from datetime import datetime
from .utils.crawler import update_drama


class DramaListView(LoggingMixin, generics.ListAPIView):
    """
        방영중인 드라마 리스트를 불러오는 API

        ---
        # Query Params
            - onair : String[true, false]
            - page : Integer
    """
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer

    def get(self, request, *args, **kwargs):
        query_params = request.query_params.get('onair')
        if query_params == 'true':
            days_of_week = ['월', '화', '수', '목', '금', '토', '일']
            queryset = Drama.objects.filter(is_broadcasting=True,
                                            broadcasting_day__name__in=[days_of_week[datetime.today().weekday()]],
                                            broadcasting_start_time__lte=datetime.now(),
                                            broadcasting_end_time__gte=datetime.now())
        else:
            queryset = Drama.objects.filter(is_broadcasting=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = sorted(serializer.data, key=lambda x: x['is_bookmarked_by_me'], reverse=True)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = sorted(serializer.data, key=lambda x: x['is_bookmarked_by_me'], reverse=True)
        return Response(data)


class DramaEachEpisodeList(LoggingMixin, APIView):
    """
        해당 드라마의 회차별 고구마, 사이다 개수 리스트를 불러오는 API

        ---
        # Query Params
            - drama_id : Integer
    """

    def get(self, request, drama_id, format=None):
        drama = Drama.objects.get(id=drama_id)
        queryset = DramaEachEpisode.objects.filter(drama=drama)
        serializer = DramaEachEpisodeSerializer(queryset, many=True)
        data = sorted(serializer.data, key=lambda x : int(x['episode']), reverse=True)

        return Response(data=data, status=status.HTTP_200_OK)
