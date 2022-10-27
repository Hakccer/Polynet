from django.contrib import admin
from hero.models import UserData, Poster, Mess

# Register your models here.
admin.site.register(UserData)


@admin.register(Mess)
class MessModelAdmin(admin.ModelAdmin):
    list_display = ['chat_name', 'users', 'messages']


@admin.register(Poster)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ["user", "main_img", "post_count"]
