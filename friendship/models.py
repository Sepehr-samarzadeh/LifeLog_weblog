from django.db import models
from users.models import User

class Friendship(models.Model):
    request_from=models.ForeignKey(to=User,on_delete=models.PROTECT,related_name='request_sender')
    request_to=models.ForeignKey(to=User,on_delete=models.PROTECT,related_name='request_receiver')
    is_accepted=models.BooleanField(default=False)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='friendship'
        verbose_name_plural='friendship'
        unique_together=('request_sender','request_receiver')
