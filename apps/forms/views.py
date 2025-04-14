from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Forms
from .serializers import FormsSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_forms(request):
    forms = Forms.objects.all().order_by('-created_at')
    serializer = FormsSerializer(forms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def create_form(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    fullname = request.data.get('fullname')
    phone = request.data.get('phone')
    email = request.data.get('email')
    forms = Forms.objects.create(
        subject=subject, message=message,
        fullname=fullname,
        phone=phone,
        email=email
    )
    return Response({"message": "News created successfully!"}, status=201)
