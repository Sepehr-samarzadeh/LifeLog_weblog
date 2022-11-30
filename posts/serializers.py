from rest_framework import serializers
from .models import Post,File,Like



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('user','title','text','is_enable',)
        extra_kwargs={
            "user":{"read_only":True}
        }




class FileSerializer(serializers.ModelSerializer):
    file_type=serializers.SerializerMethodField
    class Meta:
        model=File
        fields=('id','title','file','file_type')

    def get_file_type(self,obj):
        return obj.get_file_type_display()





class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=('post','user','is_liked','is_unliked')
        extra_kwargs={
            "post":{"read_only":True},
            "user":{"read_only":True},
            "is_liked":{"reqired":False},
            "is_unliked":{"required":False}
        }
