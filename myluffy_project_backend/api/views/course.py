from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api.models import *
from api.utils.serializer import CourseSerializers,CourseDetailSerializers,CourseCategorySerializer
from api.utils.auth import LoginAuth
from api.utils.filter import CourseFilter


class CourseView(ModelViewSet):
    # authentication_classes = [LoginAuth,]
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    filter_backends = [CourseFilter, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({"error_no": 0, "data": serializer.data})




class CourseDetailView(ModelViewSet):
    queryset = CourseDetail.objects.all()
    serializer_class = CourseDetailSerializers

class CourseCategoryView(ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"error_no":0,"data":serializer.data})