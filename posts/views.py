from rest_framework.views import APIView,status
from rest_framework.response import Response
from .serializers import PostSerializer,FileSerializer,LikeSerializer
from .models import Post,Like,File
from rest_framework.permissions import IsAuthenticated


class PostListView(APIView):
    def get(self,request):
        posts=Post.objects.filter(is_enable=True)
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_pk):
        try:
            post=Post.objects.filter(pk=post_pk,user=request.user)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=PostSerializer(post,)
        return Response(serializer.data)

    def post(self,request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    def get_post(self,post_pk):
        try:
            post=Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return False

    def get(self,request,post_pk):
        post=self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes=post.likes.filter(is_liked=True).count()
        unlikes=post.likes.filter(is_unliked=True).count()
        return Response({"likes":likes},{"unlikes":unlikes})


    def post(self,request,post_pk):
        post=self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post,user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class FileListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_pk):
        files=File.objects.filter(post_pk=post_pk)
        serializer=FileSerializer(files,many=True)
        return Response(serializer.data)


class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_pk,pk):
        try:
            file=File.objects.get(pk=pk,post_pk=post_pk)
        except File.DoesNotExit:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=FileSerializer(file)
        return Response(serializer.data)

