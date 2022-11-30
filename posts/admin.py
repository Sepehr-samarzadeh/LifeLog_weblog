from django.contrib import admin
from .models import Post,File,Like



class FileinInlineAdmin(admin.StackedInline):
    model=File
    fields = ['title','file','file_type','is_enable']
    extra=0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ['title','user','is_enable','created_time']
   inlines = [FileinInlineAdmin]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display =['post','user','is_liked','is_unliked']
    list_filter = ['is_liked','is_unliked']
    date_hierarchy = 'created_time'
