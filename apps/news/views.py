import html2json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializer
from django.shortcuts import redirect
from django_quill.quill import QuillParseError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from bs4 import BeautifulSoup

def html_to_json(html_content):
    try:
        # چاپ محتوای HTML برای بررسی
        print("Received HTML content:", html_content)

        # سانیتایز کردن محتوای HTML
        soup = BeautifulSoup(html_content, "html.parser")


        sanitized_html = str(soup)
        print("Sanitized HTML:", sanitized_html)
        
        h = html2json.HTML2Json()
        content_json = h.convert(sanitized_html)
        
        # چاپ نتیجه تبدیل به JSON
        print("Converted Content JSON:", content_json)
        
        return content_json
    except Exception as e:
        print("Error during HTML to JSON conversion:", str(e))
        return None



class BaseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def handle_unauthenticated(self, request):
        if not request.user.is_authenticated:
            return redirect('/admin/login')
        return None

class NewsAPIView(BaseAPIView):

    def get(self, request, pk=None):
        """
        گرفتن یک خبر با شناسه یا همه اخبار
        """
        if pk:
            try:
                news_item = News.objects.get(pk=pk)
            except News.DoesNotExist:
                return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            serializer = NewsSerializer(news_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return self.get_all(request)

    def get_all(self, request):
        """
        گرفتن همه اخبار
        """
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        content = request.data.get("content")
        slug = request.data.get("slug")
        image = request.FILES.get("image")


        print("Received Title:", title)  # چاپ داده‌ها برای بررسی
        print("Received Content:", content)
        print("Received Slug:", slug)
        if not title or not content:
            return Response({"detail": "عنوان و محتوا الزامی هستند."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # تبدیل محتوای HTML به فرمت JSON
            print("!@#!$@!%!^!$^@$#^#%!#%!#%!%!#!#$$#%$#!%$#!%#!#!%!$#%#$@#$")
            content_json = html_to_json(content)
            # ایجاد خبر جدید با محتوای JSON
            news = News.objects.create(
                title=title,
                content=content_json,
                slug=slug,
                image=image
            )

            return Response({"message": "News created successfully!"}, status=status.HTTP_201_CREATED)

        except QuillParseError as e:
            return Response({"error": f"Failed to parse content: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        ویرایش خبر
        """
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"detail": "خبر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')

        if content:
            try:
                # تبدیل محتوای HTML به JSON
                content_json = html_to_json(content)
            except QuillParseError:
                return Response({"detail": "محتوا به درستی قابل parse نیست."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "محتوا نمی‌تواند خالی باشد."}, status=status.HTTP_400_BAD_REQUEST)

        # بروزرسانی محتوا
        news_item.content = content_json
        news_item.title = request.data.get('title', news_item.title)
        news_item.slug = request.data.get('slug', news_item.slug)

        if 'image' in request.FILES:
            news_item.image = request.FILES['image']
        
        news_item.save()

        serializer = NewsSerializer(news_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
