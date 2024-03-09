from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

# Create your models here.
''' 
    username
    password 
    first_name
    last_name
    email  
     '''

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11,null=True , blank=True,
                                    validators=[
                                    RegexValidator(
                                    regex=r'^01\d{9}$',
                                    message='Phone number must start with 01 and be 9 digits long.',
                                    code='invalid_phone_number',
            ),
        ],)
    addres = models.CharField(max_length=50 , blank=True, null=True)
    image= models.ImageField(upload_to='users/images',blank=True,null=True)
    # image
    # age
    # Job

    def __str__(self):
        return str(self.user)

# class Profile(models.Model):
#     user = models.OneToOneField(User , on_delete=models.CASCADE)
#     phone_number = models.CharField(
#         max_length=11,
#         null=True,
#         blank=True,
#         validators=[
#             RegexValidator(
#                 regex=r'^01\d{9}$',
#                 message='Phone number must start with 01 and be 10 digits long.',
#                 code='invalid_phone_number',
#             ),
#         ],
#     )
#     addres = models.CharField(max_length=50 , blank=True, null=True)
#     image= models.ImageField(upload_to='users/images',blank=True,null=True)


@receiver(post_save , sender=User)
def create_user_profile(sender,instance,created , **kwargs):
    if created:
        Profile.objects.create(
            user = instance
        )
