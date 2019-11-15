from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Drama, DramaSerializer, DramaEachEpisode, DramaEachEpisodeSerializer
from datetime import datetime
from .utils.crawler import update_drama


class DramaListView(generics.ListAPIView):
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
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DramaEachEpisodeList(APIView):
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

        return Response(data=serializer.data, status=status.HTTP_200_OK)
