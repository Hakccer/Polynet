from django.db import models
from django.contrib.auth.models import User
import os
import json

# Create your models here.


def profile_img_upload(self, filename):
    return os.path.join("avatar", f"{self.main_user.id}")


class CustomUserObject(models.Manager):
    def starts_with(self, query):
        my_all_data = self.all()
        empty_list = []
        for i in my_all_data:
            if query.lower() == i.username[0:len(query)].lower():
                empty_list.insert(0, i)
                continue
            if query.lower() in i.username.lower():
                empty_list.append(i)
        return empty_list


def post_url(self, filename):
    return os.path.join("posts", f"{self.user.id}", f"{self.post_count()}")


class Poster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_img = models.ImageField(upload_to=post_url, blank=True)
    caption = models.TextField(
        default="The Guy Has Not Setted Any Caption For This Post So Now This is The Property of Polynet Official Thank you :)")
    likes = models.IntegerField(default=0)
    peoples = models.TextField(default=json.dumps([]))

    def post_count(self):
        return len(Poster.objects.filter(user=self.user))


class UserData(models.Model):
    main_user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    pro_img = models.ImageField(upload_to=profile_img_upload, blank=True)
    bio = models.TextField(default=f"Hello I Am Busy Now a Days")
    evolved = CustomUserObject()
    followers = models.TextField(default=json.dumps([]))
    following = models.TextField(default=json.dumps([]))
    foll_pending = models.TextField(default=json.dumps([]))
    activity = models.TextField(default=json.dumps([]))

    def get_user_name(self):
        return self.main_user.username


class Mess(models.Model):
    chat_name = models.CharField(blank=False, max_length=500)
    users = models.TextField(blank=False)
    messages = models.TextField(default=json.dumps([]))
