from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .models import Subnews
from .serializers import SubnewsSerializer

class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SubnewsAPIView(BaseAPIView):
    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

    # GET_ALL
    def get(self, request):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        subnews = Subnews.objects.all()
        serializer = SubnewsSerializer(subnews, many=True)
        return Response(serializer.data)

    # CREATE
    def post(self, request):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        serializer = SubnewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubnewsDetailAPIView(BaseAPIView):

    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

    # GET ONE
    def get(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        subnews = Subnews.objects.get(pk=pk)
        serializer = SubnewsSerializer(subnews)
        return Response(serializer.data)

    # UPDATE (FULL UPDATE)
    def put(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        subnews = Subnews.objects.get(pk=pk)
        serializer = SubnewsSerializer(subnews, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PARTIAL_UPDATE
    def patch(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        subnews = Subnews.objects.get(pk=pk)
        serializer = SubnewsSerializer(subnews, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE (ONE)
    def delete(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        subnews = Subnews.objects.get(pk=pk)
        subnews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
