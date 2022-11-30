from django.db import models




class Post(models.Model):
    user=models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    text=models.TextField()
    is_enable=models.BooleanField(default=True)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posts'

    def __str__(self):
        return self.title





class Like(models.Model):
    post=models.ForeignKey(to=Post,related_name='likes',on_delete=models.CASCADE)
    user=models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    is_liked=models.BooleanField(default=True)
    is_unliked=models.BooleanField(default=False)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)


class File(models.Model):
    FILE_IMAGE=1
    FILE_VIDEO=2
    FILE_PDF=3

    FILE_TYPE_CHOICES=(
        (FILE_IMAGE,('image')),
        (FILE_VIDEO,('video')),
        (FILE_PDF,('pdf'))
    )
    post=models.ForeignKey(to='Post',verbose_name='post',related_name='files',on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    file_type=models.PositiveSmallIntegerField(choices=FILE_TYPE_CHOICES)
    file=models.FileField(upload_to='files%Y%M%D')
    is_enable=models.BooleanField(default=True)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='post file'
        verbose_name_plural='post files'




