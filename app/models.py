from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(
        max_length=15, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now)
    liked = models.ManyToManyField('Post', related_name='liked_by',
                                   db_table='profile_post_1', blank=True)

    class Meta:
        db_table = "profile"
        
    def __str__(self):
        return self.username


class Post(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now)
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='posts')

    class Meta:
        db_table = "post"
        
    def __str__(self):
        return self.title

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    print("post_save_user_model_receiver", instance)
    if created:
        try:
            p = Profile(user=instance, username=instance.username, created_at=instance.date_joined)
            p.save()
        except e:
            print("Error:", e)


post_save.connect(post_save_user_model_receiver,
                  sender=settings.AUTH_USER_MODEL)
