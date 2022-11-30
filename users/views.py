import random
import uuid

from rest_framework.views import APIView,status
from rest_framework.response import Response
from .models import User,Device
from django.core.cache import cache

class RegisterView(APIView):
    def post(self,request):
        email=request.data.get('email')
        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            user=User.objects.create_user(email=email)
        device=Device.objects.create(user=user)
        code=random.randint(10000,99999)
        #send email
        #cache
        cache.set(email,code,2*60)
        return Response({"code":code})

class GetTokenView(APIView):
    def post(self,request):
        email=request.data.get('email')
        code=request.data.get('code')
        cached_code=cache.get(email)
        if code!=cached_code:
            return Response(status=status.HTTP_403_FORBIDDEN)
        token=str(uuid.uuid4())
        return Response({"token":token})

