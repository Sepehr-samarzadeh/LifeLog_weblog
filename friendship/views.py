from rest_framework.views import APIView,status
from rest_framework.response import Response
from.models import Friendship
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from users.models import User
from friendship.serializers import UserListSerializer



class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        q=request.query_params.get('q')
        if q:
            users=User.objects.filter(username_icontains=q)
        else:
            users=User.objects.all()
            serializer=UserListSerializer(users,many=True)
            return Response(serializer.data)

class RequestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_id=request.data.get('user')
        try:
            user=User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.get_or_create(request_sender=request.user,request_receiver=user)
        return Response({"detail":"request sent"},status=status.HTTP_201_CREATED)



class RequestListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        friendship=Friendship.objects.filter(request_receiver=request.user,is_accepted=False)
        users=[fr.request_sender for fr in friendship]
        serializer=UserListSerializer(users,many=True)
        return Response(serializer.data)


class AcceptView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_id=request.data.get('user')
        try:
            user=User.objects.get(pk=user_id)
            friendship=Friendship.objects.get(request_sender=user,request_receiver=request.user,is_accepted=False)
        except(User.DoesNotExist,Friendship.DoestNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        friendship.is_accepted=True
        friendship.save()
        return Response({"detail":"connected"})


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        friendship=Friendship.objects.filter(
            Q(request_sender_id=request.user) | Q(request_receiver=request.user),
            is_accepted=True
        )
        users=[fr.request_sender for fr in friendship]
        serializer=UserListSerializer(users,many=True)
        return Response(serializer.data)









