from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import NewsSerializer
from .models import News
from rest_framework.response import Response


class NewsListAPIViews(GenericAPIView, ListModelMixin):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        queryset = News.objects.all()
        tags = self.request.query_params.getlist('tags')

        if tags:
            queryset = set(queryset.filter(tags__name__in=tags))

        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)


