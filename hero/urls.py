from django.contrib import admin
from django.urls import path
from hero.views import *
from hero.auths import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# def_route = DefaultRouter()
# def_route.register('only_mess', ManageMessage, basename="Only Messages")


urlpatterns = [
    path('', home, name="Home"),
    path('signup', signer, name="SignUp"),
    path('login', CustomObtainToken.as_view(), name="Login"),
    path('verify', verify_acc, name="Verify Person"),
    path('search', get_search, name="Search User"),
    path('profile', get_profile, name="Profile"),
    path('add_post', add_post, name="Adding Posts Here"),
    path('get_guy/', getting_guy, name="getting Poeple By-This"),
    path('follow_guy', handle_follow,
         name="It Will Going to Handle All the Following Process"),
    path('my_followings', get_following, name="getting My Followings"),
    path('my_followers', get_followers, name="getting My Followers"),
    path('all_posts', get_all_posts, name="All Posts"),
    path('like_post', handle_like, name="Post Likes"),
    path('get_activity', get_activity, name="My Activity"),
    path('remove_token', remove_me, name="Removing My Self from login"),
    path('get_mess_people', mess_people, name="Getting mess people"),
    path('only_mess/<slug:slug>', ManageMessage.as_view(),
         name="Getting Only Messsages"),
    path('only_mess', ManageMessage.as_view(),
         name="Sending Only Messsages"),
    path('manage_me', ManageProfile.as_view(), name="Managing Your Profile"),
    path('change_pass', ManagePassChange.as_view(), name="Changing Password"),
    path('new_pass', update_pass, name="Update_pass")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += def_route.urls
