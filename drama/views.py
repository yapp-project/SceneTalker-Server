from rest_framework import generics
from rest_framework.response import Response
from .models import Drama, DramaSerializer
from datetime import datetime
from .utils.crawler import update_drama


class DramaListView(generics.ListAPIView):
    """
        방영중인 드라마 리스트를 불러오는 API

        ---
        # Query Params
            - onair : String[true, false]
            - page : Integer
        # Response
            - id : 드라마 id
            - title : 드라마 제목
            - summary : 줄거리
            - genre : 장르
            - rating : 시청률
            - poster_url : 포스터 url
            - broadcasting_day : 방송요일
            - broadcasting_start_time : 방송 시작시간
            - broadcasting_end_time : 방송 종료시간
            - broadcasting_station : 방송국
            - is_broadcasting : 방영중 여부
            - is_bookmarked_by_me : 사용자가 북마크했는지 여부
            - episode : 부
            - created_at : 생성시간
            - updated_at : 수정시간
            - feed : 피드정보
                - id : 피드 id
                - drama : 드라마 id
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
