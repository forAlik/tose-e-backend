from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .models import Achievements
from .serializers import AchievementsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny


class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return super().get_permissions()
class AchievementsAPIView(BaseAPIView):
    
    # GET_ALL
    def get(self, request):
        achievements = Achievements.objects.all()
        serializer = AchievementsSerializer(achievements, many=True)
        return Response(serializer.data)

    # CREATE
    def post(self, request):
        serializer = AchievementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AchievementsDetailAPIView(BaseAPIView):

    def get_object(self, pk):
        try:
            return Achievements.objects.get(pk=pk)
        except Achievements.DoesNotExist:
            return None

    # GET
    def get(self, request, pk):
        achievement = self.get_object(pk)
        if achievement:
            serializer = AchievementsSerializer(achievement)
            return Response(serializer.data)
        return Response({"error": "دستاورد یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    # UPDATE
    def put(self, request, pk):
        achievement = self.get_object(pk)
        if achievement:
            serializer = AchievementsSerializer(achievement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "دستاورد یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE
    def delete(self, request, pk):
        achievement = self.get_object(pk)
        if achievement:
            achievement.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "دستاورد یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
