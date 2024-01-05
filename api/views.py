from http import HTTPStatus
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from api.serializers import *

from home.models import DeviceLog

class DeviceLogView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = DeviceLogSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()   
        return Response(data={
            'message': 'Record Created.',
            'success': True
        }, status=HTTPStatus.OK)