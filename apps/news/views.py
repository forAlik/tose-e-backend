from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import News
from .serializers import NewsSerializer
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny


class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

class NewsAPIView(BaseAPIView):

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk=None, slug=None):
        """
        دریافت یک خبر خاص یا همه اخبار
        """
        if pk and not slug:
            try:
                news_item = News.objects.get(pk=pk)
            except News.DoesNotExist:
                return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            serializer = NewsSerializer(news_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif slug:
            try:
                news_item = News.objects.get(slug=slug)
            except News.DoesNotExist:
                return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            serializer = NewsSerializer(news_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return self.get_all(request)

    def get_all(self, request):
        """
        دریافت همه اخبار
        """
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        slug = request.data.get('slug')
        image = request.FILES.get('image')

        news = News.objects.create(
            title=title,
            content=content,
            slug=slug,
            image=image
        )
        return Response({"message": "News created successfully!"}, status=201)

    def put(self, request, *args, **kwargs):
        news = News.objects.get(id=kwargs.get('pk'))
        news.title = request.data.get('title', news.title)
        news.content = request.data.get('content', news.content)
        news.slug = request.data.get('slug', news.slug)

        image = request.FILES.get('image')
        if image:
            news.image = image

        news.save()
        return Response({"message": "News updated successfully!"})

    def patch(self, request, *args, **kwargs):
        try:
            news = News.objects.get(id=kwargs.get('pk'))
        except News.DoesNotExist:
            return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        
        if 'title' in request.data:
            news.title = request.data['title']
        if 'content' in request.data:
            news.content = request.data['content']
        if 'slug' in request.data:
            news.slug = request.data['slug']

        image = request.FILES.get('image')
        if image:
            news.image = image

        news.save()
        return Response({"message": "News partially updated successfully!"})
    
    def delete(self, request, pk=None):
        """
        حذف یک خبر
        """
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        news_item.delete()
        return Response({"detail": "خبر با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)
