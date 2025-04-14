from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Subnews
from .serializers import SubnewsSerializer


class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class SubnewsAPIView(BaseAPIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    # GET_ALL
    def get(self, request):
        subnews = Subnews.objects.all()
        serializer = SubnewsSerializer(subnews, many=True)
        return Response(serializer.data)

    # CREATE
    def post(self, request):
        serializer = SubnewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubnewsDetailAPIView(BaseAPIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    # GET ONE
    def get(self, request, pk):
        subnews = get_object_or_404(Subnews, pk=pk)
        serializer = SubnewsSerializer(subnews)
        return Response(serializer.data)

    # FULL UPDATE
    def put(self, request, pk):
        subnews = get_object_or_404(Subnews, pk=pk)
        serializer = SubnewsSerializer(subnews, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PARTIAL UPDATE
    def patch(self, request, pk):
        subnews = get_object_or_404(Subnews, pk=pk)
        serializer = SubnewsSerializer(subnews, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        subnews = get_object_or_404(Subnews, pk=pk)
        subnews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)