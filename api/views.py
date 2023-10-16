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

    # def get(self, request, pk=None):
    #     if not pk:
    #         return Response({
    #             'data': [DeviceLogSerializer(instance=obj).data for obj in DeviceLog.objects.all()],
    #             'success': True
    #         }, status=HTTPStatus.OK)
    #     try:
    #         obj = get_object_or_404(DeviceLog, pk=pk)
    #     except Http404:
    #         return Response(data={
    #             'message': 'object with given id not found.',
    #             'success': False
    #         }, status=HTTPStatus.NOT_FOUND)
    #     return Response({
    #         'data': DeviceLogSerializer(instance=obj).data,
    #         'success': True
    #     }, status=HTTPStatus.OK)

    # def put(self, request, pk):
    #     try:
    #         obj = get_object_or_404(DeviceLog, pk=pk)
    #     except Http404:
    #         return Response(data={
    #             'message': 'object with given id not found.',
    #             'success': False
    #         }, status=HTTPStatus.NOT_FOUND)
    #     serializer = DeviceLogSerializer(instance=obj, data=request.data, partial=True)
    #     if not serializer.is_valid():
    #         return Response(data={
    #             **serializer.errors,
    #             'success': False
    #         }, status=HTTPStatus.BAD_REQUEST)
    #     serializer.save()
    #     return Response(data={
    #         'message': 'Record Updated.',
    #         'success': True
    #     }, status=HTTPStatus.OK)

    # def delete(self, request, pk):
    #     try:
    #         obj = get_object_or_404(DeviceLog, pk=pk)
    #     except Http404:
    #         return Response(data={
    #             'message': 'object with given id not found.',
    #             'success': False
    #         }, status=HTTPStatus.NOT_FOUND)
    #     obj.delete()
    #     return Response(data={
    #         'message': 'Record Deleted.',
    #         'success': True
    #     }, status=HTTPStatus.OK)

