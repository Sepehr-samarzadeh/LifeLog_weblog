import random

from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager



class UserManager(BaseUserManager):

    use_in_migrations=True

    def _create_user(self,username,email,password,is_staff,is_superuser,**extra_fields):
        now=timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email=self.normalize_email(email)
        user=self.model(
            username=username,email=email,
            is_staff=is_staff,is_active=True,
            is_superuser=is_superuser,date_joined=now,
            **extra_fields
        )
        if not extra_fields.get('no_password'):
            user.set_password(password)
            user.save(using=self.db)
            return user

    def create_user(self,username=None,email=None,password=None,**extra_fields):
        if username is None:
            if email:
                username=email.split('@',1)[0]
            while User.objects.filter(username=username).exist():
                username +=str(random.randint(10,99))

            return self._create_user(username,email,password,False,False,**extra_fields)

    def create_superuser(self,username,email,password,**extra_fields):
        return self._create_user(username,email,password,True,True,**extra_fields)


class User(AbstractUser,PermissionsMixin):
    username=models.CharField('username',max_length=10,unique=True,
                              help_text='need 10 characters or fewer',
                              validators=[validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                              'Enter a valid username starting with a-z. '
                                                                'This value may contain only letters, numbers '
                                                                'and underscore characters.', 'invalid')




                                          ],
                              error_messages={
                                  'unique':'a user with the same username is already exist'
                              }




                              )
    first_name =models.CharField('first name',max_length=10,blank=True)
    last_name =models.CharField('last name',max_length=20,blank=True)
    email =models.EmailField('email address',unique=True)
    is_staff = models.BooleanField('staff status',default=False,)
    is_active = models.BooleanField('active',default=True)
    date_joined = models.DateTimeField('date joined',default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name='user'
        verbose_name_plural='users'


class ProfileUser(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE)
    nick_name=models.CharField('nickname',max_length=10,blank=True)
    avatar=models.ImageField('avatar',blank=True,upload_to='profile_avatar/')
    birthday=models.DateField('birthday',null=True,blank=True)

    class Meta:
        verbose_name='user profile'
        verbose_name_plural='user profiles'




class Device(models.Model):
    WEB=1
    IOS=2
    ANDROID=3

    DEVICE_TYPE_CHOICES=(
        (WEB,'web'),
        (IOS,'ios'),
        (ANDROID,'android')

    )
    user=models.ForeignKey(to=User,related_name='devices',on_delete=models.CASCADE)
    device_uuid=models.UUIDField('Device UUID',null=True)
    device_type=models.PositiveSmallIntegerField('device type',choices=DEVICE_TYPE_CHOICES,default=WEB)
    last_login=models.DateTimeField('last login',null=True)
    created_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='user_device'
        verbose_name_plural='user_devices'
        unique_together='user','device_uuid'









