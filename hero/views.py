from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.admin import User
from hero.serializer import UserSerializer, PostSerizlier
from django.core.cache import cache
import random
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from hero.models import UserData, Poster
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
import json
import random
from datetime import datetime
from hero.serializer import *
# Create your views here.


@api_view(['GET', 'POST'])
def home(request):
    my_user = User.objects.all()
    serial_user = UserSerializer(data=my_user, many=True)
    serial_user.is_valid()
    return Response({
        'culer': serial_user.data
    }, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_search(request):
    query = request.GET.get('query')
    my_all_data = User.objects.all()
    print(query)
    if query == '':
        my_lister = []
        for k in User.objects.all():
            try:
                my_lister.append({
                    'u_name': k.username,
                    'u_real': k.first_name,
                    'u_bio': UserData.evolved.get(main_user=k).bio,
                    'u_atr': UserData.evolved.get(main_user=k).pro_img.name
                })
            except Exception as e:
                pass
        return Response({
            'data': my_lister
        })

    empty_list = []
    for i in my_all_data:
        print(i)
        if query.lower() == i.username[0:len(query)].lower():
            try:
                print("This Works")
                empty_list.insert(0, {
                    'u_name': i.username,
                    'u_real': i.first_name,
                    'u_bio': UserData.evolved.get(main_user=i).bio,
                    'u_atr': UserData.evolved.get(main_user=i).pro_img.name
                })
            except Exception as e:
                continue
            continue
        if query.lower() in i.username.lower():
            try:
                print("This Works")
                empty_list.append({
                    'u_name': i.username,
                    'u_real': i.first_name,
                    'u_bio': UserData.evolved.get(main_user=i).bio,
                    'u_atr': UserData.evolved.get(main_user=i).pro_img.name
                })
            except Exception as e:
                continue
    print(empty_list)
    return Response({
        'data': empty_list
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getting_guy(request):
    is_following = False
    guy_name = request.GET.get('username')
    my_token = str(request.headers.get('Authorization')).split(" ")[1]
    my_user = User.objects.filter(username=guy_name)[0]
    my_user_data = UserData.evolved.filter(main_user=my_user)[0]
    all_posts = Poster.objects.filter(
        user=my_user)
    my_serial_posts = JSONRenderer().render(
        PostSerizlier(all_posts, many=True).data)
    my_self = Token.objects.filter(key=my_token)[0].user

    if my_self.id in json.loads(my_user_data.followers):
        is_following = True

    return Response({
        'n_name': my_user.first_name,
        'idel': my_user.id,
        'u_name': my_user.username,
        'p_imgs': my_user_data.pro_img.name,
        'b_bios': my_user_data.bio,
        'f_fall': json.loads(my_user_data.followers),
        'm_fall': json.loads(my_user_data.following),
        'posts': my_serial_posts,
        'a_fall': is_following
    })


@api_view(['POST'])
def signer(request):
    mail_error = "correct"
    name_error = "correct"
    user_error = "correct"
    pass_error = "correct"

    print(request.data)

    for i, j in request.data.items():
        if j == "":
            return Response({
                'glob': True,
                'error': "All The Fields Must Be Filled"
            })

    if "@" not in request.data['emas'].lower():
        mail_error = "Invalid email try again"

    if len(request.data['emas']) <= 5:
        mail_error = "Email is too small try again"

    if len(User.objects.filter(email=request.data['emas'])) > 0:
        mail_error = "User With This Email Already registered"

    if len(request.data['nams']) < 3:
        name_error = "Name is Too Short try again"

    if len(str(request.data['nams']).split(" ")) > 2:
        name_error = "Name is Invalid should only contain one space"

    if len(request.data['uses']) < 5:
        user_error = "username is too short try again"

    if len(User.objects.filter(username=request.data['uses'])) > 0:
        user_error = "Username Already taken try another one"

    if len(request.data['pass']) < 8:
        pass_error = "Password is too small try again with a bigger one"

    return Response({
        'my_err': [mail_error, name_error, user_error, pass_error]
    })


def sending_mail(gmail, token):
    subject = "Polynet Wants Your Profile Needs to be verified"
    message = f"Paste This OTP in Authentication Field {token}"
    sender = settings.EMAIL_HOST_USER
    reciptent = [gmail]
    send_mail(subject, message, sender, reciptent)


def get_randon_numbs():
    my_opt = ""
    for i in range(6):
        my_opt += str(random.randint(0, 9))
    return my_opt


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    my_token = request.headers.get('Authorization')
    my_user = Token.objects.filter(key=str(my_token).split(" ")[1])[0].user
    my_user_data = UserData.evolved.filter(main_user=my_user)[0]
    all_posts = Poster.objects.filter(
        user=my_user)

    my_serial_posts = JSONRenderer().render(
        PostSerizlier(all_posts, many=True).data)

    return Response({
        'n_name': my_user.first_name,
        'u_name': my_user.username,
        'p_imgs': my_user_data.pro_img.name,
        'b_bios': my_user_data.bio,
        'f_fall': json.loads(my_user_data.followers),
        'm_fall': json.loads(my_user_data.following),
        'posts': my_serial_posts
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    my_token = request.headers.get('Authorization').split(" ")[1]
    pos = request.data['post']
    caption = request.data['cap']
    my_post = Poster.objects.create(
        user=Token.objects.filter(key=my_token)[0].user, caption=caption)
    my_post.main_img.save(
        pos.name, pos, save=True
    )

    return Response({
        'success': 'Image Uploaded Successfully'
    })


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_posts(request):
#     my_token = str(request.headers.get('Authorization')).split(" ")[0]


@api_view(['GET', 'POST'])
def verify_acc(request):
    if request.method == 'GET':
        your_mail = request.GET.get("email")
        print(your_mail)
        my_generated_otp = get_randon_numbs()
        my_mail = cache.get(your_mail)
        print(my_mail)
        if my_mail != None:
            return Response({
                'resend_error': "You Cannot Resend Otp Before 60 Seconds"
            })
        cache.set(your_mail, my_generated_otp, 60)
        sending_mail(str(your_mail), my_generated_otp)
        return Response({
            'res': "Email Sended"
        })
    if request.method == 'POST':
        your_otp = request.data['otp']
        your_mail = request.data['email']
        real_otp = cache.get(your_mail)
        if real_otp == your_otp:
            if len(User.objects.filter(email=str(your_mail))) <= 0:
                my_user = User.objects.create(email=str(your_mail),
                                              username=str(
                                                  request.data['user']),
                                              first_name=str(request.data['name']))
                my_user.set_password(request.data['pass'])
                my_user.save()

                UserData.evolved.create(main_user=my_user)
            return Response({
                'ok': True
            })
        else:
            return Response({
                'ok': False
            })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def handle_follow(request):
    my_token = str(request.headers.get('Authorization')).split(" ")[1]
    p_user = User.objects.filter(id=str(request.data['user_id']))[0]
    m_user = Token.objects.filter(key=my_token)[0].user

    # Our Data Variables -//-
    p_user_data = UserData.evolved.filter(main_user=p_user)[0]
    m_user_data = UserData.evolved.filter(main_user=m_user)[0]

    print("sdsw")

    guy_followers = list(json.loads(p_user_data.followers))
    activity_list = list(json.loads(p_user_data.activity))
    my_following = list(json.loads(m_user_data.following))

    print("sd")
    print(m_user)

    if m_user.id not in guy_followers:
        guy_followers.append(m_user.id)
        my_following.append(p_user.id)
        activity_list.append({
            'u_id': m_user.id,
            'func': 'following you',
            'time': str(datetime.now().strftime("%H:%M %p")),
            'Date': str(datetime.now().strftime("%d/%m/%Y"))
        })
    else:
        guy_followers.remove(m_user.id)
        my_following.remove(p_user.id)
        activity_list.append({
            'u_id': m_user.id,
            'func': 'unfollowing you',
            'time': str(datetime.now().strftime("%H:%M %p")),
            'Date': str(datetime.now().strftime("%d/%m/%Y"))
        })
    print("sd")
    UserData.evolved.filter(main_user=p_user).update(
        followers=json.dumps(guy_followers))
    UserData.evolved.filter(main_user=m_user).update(
        following=json.dumps(my_following))
    UserData.evolved.filter(main_user=p_user).update(
        activity=json.dumps(activity_list))
    return Response({
        's': 'Successfully Runned Here'
    })


@ api_view(['GET'])
@ authentication_classes([TokenAuthentication])
@ permission_classes([IsAuthenticated])
def get_following(request):
    try:
        my_token = str(request.headers.get('Authorization')).split(" ")[1]

        # My Followings In One Line here:
        my_followings = json.loads(UserData.evolved.filter(
            main_user=Token.objects.filter(key=my_token)[0].user)[0].following)

        my_users = []
        for i in my_followings:
            cur_user = User.objects.get(id=i)
            cur_user_data = UserData.evolved.get(main_user=cur_user)
            my_users.append({
                'u_name': cur_user.username,
                'u_real': cur_user.first_name,
                'u_bio': cur_user_data.bio,
                'u_atr': cur_user_data.pro_img.name
            })
        return Response({
            's': my_users
        })
    except Exception as e:
        return Response({
            's': 'Something Went Wrong'
        })

# For Getting All The Feeds Posts


@ api_view(['GET'])
@ authentication_classes([TokenAuthentication])
@ permission_classes([IsAuthenticated])
def get_all_posts(request):

    # Single Line Function For Getting the Followings Result
    my_followings = json.loads(UserData.evolved.get(
        main_user=Token.objects.get(key=request.headers.get('Authorization').split(" ")[1]).user).following)

    my_posts = []
    my_self = Token.objects.get(key=request.headers.get(
        'Authorization').split(" ")[1]).user

    my_data = UserData.evolved.get(main_user=my_self)
    for i in range(len(my_followings)):
        cur_user = User.objects.get(id=my_followings[i])
        cur_user_data = UserData.evolved.get(main_user=cur_user)
        cur_user_posts = Poster.objects.filter(user=cur_user)
        for i in cur_user_posts:
            m_like = 'white'
            pops = list(json.loads(i.peoples))
            if my_self.id in pops:
                m_like = 'red'
            my_posts.append({
                'u_name': cur_user.username,
                'r_name': cur_user.first_name,
                'a_avtr': cur_user_data.pro_img.name,
                't_post': i.main_img.name,
                't_capt': i.caption,
                'l_likes': i.likes,
                'p_peos': list(json.loads(i.peoples)),
                'k_id': i.id,
                'm_like': m_like
            })

    for k in Poster.objects.filter(user=my_self):
        m_like = 'white'
        pops = list(json.loads(k.peoples))
        if my_self.id in pops:
            m_like = 'red'
        my_posts.append({
            'u_name': my_self.username,
            'r_name': my_self.first_name,
            'a_avtr': my_data.pro_img.name,
            't_post': k.main_img.name,
            't_capt': k.caption,
            'l_likes': k.likes,
            'p_peos': list(json.loads(k.peoples)),
            'k_id': k.id,
            'm_like': m_like
        })

    random.shuffle(my_posts)
    return Response({
        'all_posts': my_posts
    })


@ api_view(['POST'])
@ authentication_classes([TokenAuthentication])
@ permission_classes([IsAuthenticated])
def handle_like(request):
    try:
        # Pre-Process Going From here
        my_self = Token.objects.get(key=request.headers.get(
            'Authorization').split(" ")[1]).user
        my_post = Poster.objects.get(id=request.data['post_id'])
        my_post_likes = list(json.loads(my_post.peoples))

        post_person = my_post.user
        post_person_data = UserData.evolved.get(main_user=post_person)

        post_person_activity = list(json.loads(post_person_data.activity))

        # Main Process Is Going From Here
        if my_self.id not in my_post_likes:
            my_post_likes.append(my_self.id)
            post_person_activity.append({
                'u_id': my_self.id,
                'func': 'like',
                'time': str(datetime.now().strftime("%H:%M %p")),
                'Date': str(datetime.now().strftime("%d/%m/%Y"))
            })
        else:
            my_post_likes.remove(my_self.id)
            post_person_activity.append({
                'u_id': my_self.id,
                'func': 'dislike',
                'time': str(datetime.now().strftime("%H:%M %p")),
                'Date': str(datetime.now().strftime("%d/%m/%Y"))
            })

        # Post Process Going From Here
        my_post.peoples = json.dumps(my_post_likes)
        my_post.save()

        post_person_data.activity = json.dumps(post_person_activity)
        post_person_data.save()
        return Response({
            'log': 'Successfully Added'
        })

    except Exception as e:
        print("Critical Error Occured")
        print(e)
        return Response({
            'error': 'lol'
        })


@ api_view(['GET'])
@ authentication_classes([TokenAuthentication])
@ permission_classes([IsAuthenticated])
def get_followers(request):
    try:
        my_token = str(request.headers.get('Authorization')).split(" ")[1]
        my_self = Token.objects.get(key=my_token).user
        print("go")
        my_self_followers = json.loads(
            UserData.evolved.get(main_user=my_self).followers)
        my_followers = []
        for i in my_self_followers:
            the_cur_user = User.objects.get(id=i)
            the_cur_user_data = UserData.evolved.get(main_user=the_cur_user)
            my_followers.append({
                'u_name': the_cur_user.username,
                'u_real': the_cur_user.first_name,
                'u_atr': the_cur_user_data.pro_img.name,
                'u_bio': the_cur_user_data.bio
            })
        return Response({
            's': my_followers
        })
    except Exception as e:
        return Response({
            'error': e
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_activity(request):
    try:
        my_token = str(request.headers.get('Authorization')).split(" ")[1]
        my_activity = list(json.loads(UserData.evolved.get(
            main_user=Token.objects.get(key=my_token).user).activity))
        send_activity = []
        for i in my_activity:
            cur_user = User.objects.get(id=i['u_id'])
            print(cur_user)
            cur_user_data = UserData.evolved.get(main_user=cur_user)
            send_activity.append({
                'p_name': cur_user.username,
                'p_avtr': cur_user_data.pro_img.name,
                'p_func': i['func'],
                'p_time': i['time'],
                'p_date': i['Date']
            })
        return Response({
            'act': send_activity
        })
    except Exception as e:
        print(e)
        return Response({
            'error': "Something is not right please try again"
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_me(request):
    try:
        my_token = str(request.headers.get('Authorization')).split(" ")[1]
        if len(Token.objects.filter(key=my_token)) > 0:
            Token.objects.filter(key=my_token).delete()
            return Response({
                "s": "Token Deleted"
            })
        else:
            return Response({
                "error": "Something Went Wrong"
            })
    except Exception as e:
        return Response({
            'error': "Something Went Wrong"
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mess_people(request):
    try:
        my_token = str(request.headers.get('Authorization')).split(" ")[1]
        my_self = Token.objects.get(key=my_token).user
        my_data = UserData.evolved.get(main_user=my_self)

        # Main Variables
        my_followings = json.loads(my_data.following)
        my_followers = json.loads(my_data.followers)

        main_peoples = []
        for i in my_followings:
            main_peoples.append(i)
        for i in my_followers:
            main_peoples.append(i)
        main_peoples = list(set(main_peoples))

        peps = []
        for i in main_peoples:
            cur_user = User.objects.get(id=i)
            cur_user_data = UserData.evolved.get(main_user=cur_user)
            peps.append({
                'u_name': cur_user.username,
                'r_name': cur_user.first_name,
                'r_avtr': cur_user_data.pro_img.name,
                'bio': cur_user_data.bio
            })
        return Response({
            'data': peps
        })
    except Exception as e:
        return Response({
            'error': "Something Went Wrong"
        })


class ManageMessage(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        print(request.user)
        my_name = request.user.username
        his_name = str(slug)

        if len(User.objects.filter(username=his_name)) == 0:
            return Response({
                'error': "User Not Found"
            })

        first_comb = my_name+his_name
        sec_comb = his_name+my_name

        if len(Mess.objects.filter(chat_name=first_comb)) == 0 and len(Mess.objects.filter(chat_name=sec_comb)) == 0:
            new_mess = Mess.objects.create(
                chat_name=first_comb,
                users=json.dumps([my_name, his_name]),
                messages=json.dumps([])
            )
            return Response({
                'room': "Created",
                'main_mess': [],
                "room_id": new_mess.id
            })

        first_comb_data = Mess.objects.filter(chat_name=first_comb)
        sec_comb_data = Mess.objects.filter(chat_name=sec_comb)

        if len(first_comb_data) > 0:
            return Response({
                's': "Success Room Already Created",
                'main_mess': json.loads(first_comb_data[0].messages),
                'room_id': first_comb_data[0].id
            })

        if len(sec_comb_data) > 0:
            return Response({
                's': "Success Room Already Created",
                'main_mess': json.loads(sec_comb_data[0].messages),
                'room_id': sec_comb_data[0].id
            })

        return Response({
            'error': "Something Went Wrong"
        })

    def post(self, request):
        my_self = request.user.username
        the_user = str(request.data['guy_name'])
        my_mess = str(request.data['message'])

        room_id_1 = the_user+my_self
        room_id_2 = my_self+the_user

        if my_mess == '':
            return Response({
                'error': 'Something Went Wrong'
            })

        print(room_id_1, room_id_2)

        if len(Mess.objects.filter(chat_name=room_id_1)) > 0:
            room = Mess.objects.filter(chat_name=room_id_1)[0]
        if len(Mess.objects.filter(chat_name=room_id_2)) > 0:
            room = Mess.objects.filter(chat_name=room_id_2)[0]

        room_messages = list(json.loads(room.messages))
        room_messages.append([str(my_self), my_mess])
        room.messages = json.dumps(room_messages)
        room.save()
        return Response({
            's': "Data Added Successfully"
        })


class ManageProfile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            my_self = request.user
            my_self_data = UserData.evolved.get(main_user=my_self)

            return Response({
                'r_name': my_self.first_name,
                'bio': my_self_data.bio,
                'pro_img': my_self_data.pro_img.name,
            })
        except Exception as e:
            print("Critical Error Occured")
            return Response({
                'error': "Something went wrong"
            })

    def post(self, request):
        try:
            all_data = request.data
            if all_data['r_name'] == "" or all_data['bio'] == "":
                return Response({
                    "error": "All the Fields Must Be Filled"
                })
            my_self = request.user
            my_data = UserData.evolved.get(main_user=my_self)
            my_self.first_name = all_data['r_name']
            my_self.save()
            my_data.bio = all_data['bio']
            my_data.save()
            my_data.pro_img.save(
                all_data['r_avtr'].name, all_data['r_avtr'], save=True)
            return Response({
                's': "Profile Updated Enjoy"
            })
        except Exception as e:
            return Response({
                'e': "Critical Error Something went wrong"
            })


class ManagePassChange(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            my_self = request.user
            tem_otp = get_randon_numbs()
            tem_mail = cache.get(my_self.email)
            if tem_mail != None:
                return Response({
                    'error': "you cannot resend otp before 60 seconds"
                })
            cache.set(my_self.email, tem_otp, 60)
            sending_mail(my_self.email, tem_otp)
            return Response({
                's': "Otp sended successfully",
                'email': str(my_self.email)
            })
        except Exception as e:
            print(e)
            return Response({
                'error': "Something went wrong please try again later"
            })

    def post(self, request):
        try:
            my_otp = request.data['my_otp']
            my_gmail = request.user.email
            if len(str(my_otp)) > 6 or len(str(my_otp)) < 6:
                return Response({
                    'error': "Invalid Otp Please Try Again"
                })
            print(my_otp, cache.get(my_gmail))
            if str(my_otp) == str(cache.get(my_gmail)):
                return Response({
                    's': "Person Verified"
                })
            else:
                return Response({
                    'error': "Wrong Otp Please Try Again Later"
                })
        except Exception as e:
            print("Critical Error Occured")
            return Response({
                'error': "Something Went Wrong Please Try Again"
            })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_pass(request):
    try:
        my_self = request.user
        first_pass = request.data['first']
        second_pass = request.data['second']
        if len(first_pass) < 8 or len(second_pass) < 8:
            return Response({
                'error': "increase the length of your password must be greater than 8 characters and must be same"
            })
        if first_pass != second_pass:
            return Response({
                'error': "Both The Fields Must Be Match"
            })
        me = User.objects.get(username=my_self.username)
        me.set_password(second_pass)
        me.save()
        return Response({
            's': "Data Updated Successfully"
        })
    except Exception as e:
        return Response({
            'error': "Something Went Wrong try again aur do the whole process from starting"
        })
