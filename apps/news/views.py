from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .models import News
from .serializers import NewsSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

class NewsAPIView(BaseAPIView):
    
    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

    # GET_ALL
    def get(self, request):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    # CREATE
    def post(self, request):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailAPIView(BaseAPIView):
    
    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return None

    # GET
    def get(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        news = self.get_object(pk)
        if news:
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        return Response({"error": "خبر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    # UPDATE
    def put(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        news = self.get_object(pk)
        if news:
            serializer = NewsSerializer(news, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "خبر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE
    def delete(self, request, pk):
        redirect_response = self.handle_unauthenticated(request)
        if redirect_response:
            return redirect_response
        news = self.get_object(pk)
        if news:
            news.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "خبر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
