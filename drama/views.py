from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Drama, DramaSerializer
from .utils.crawler import update_drama
from datetime import datetime


class DramaListCreateView(generics.ListAPIView):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer

    # 필드로 필터링할 때 사용하는데 on-air 인지 아닌지만 판단하기때문에 필드로 판단 불가해서 사용하지 않을듯
    # filter_backends = (DjangoFilterBackend, )
    # filter_fields = ('is_broadcasiting', 'broadcasting_day', 'broadcasting_start_time')

    def get(self, request, *args, **kwargs):
        if request.query_params.get('onair', True):
            days_of_week = ['월', '화', '수', '목', '금', '토', '일']
            print(Drama.objects.filter(is_broadcasiting=True,
                                       broadcasting_day__name__in=[days_of_week[datetime.today().weekday()]],
                                       broadcasting_start_time__lte=3))
            return Response()
        else:
            self.list(request, *args, **kwargs)

        # Food.objects.filter(tags__name__in=["delicious", "red"])
        # update_drama()
