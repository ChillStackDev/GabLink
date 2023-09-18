from django.shortcuts import render , redirect
import requests
from django.contrib.auth.models import User,auth
from .models import Profile
import random
from personal.models import UserProfileModel
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login 

def index(request):
    return render(request,'index.html')
def hello(request):
    return render(request,'hello.html')
# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')

def login_attempt(request):  # sourcery skip: last-if-guard
       if request.method == 'POST':
            mobile = request.POST.get('mobile')
        
            user = Profile.objects.filter(mobile = mobile).first()
        
            if user is None:
               context = {'message' : 'User not found' , 'class' : 'danger' }
               return render(request,'login.html' , context)
        
            otp = str(random.randint(1000 , 9999))
            user.otp = otp
            user.save()
            send_otp(mobile , otp)
            request.session['mobile'] = mobile
            return redirect('login_otp')        
       return render(request,'login.html')

 
def login_otp(request):
        mobile = request.session['mobile']
        context = {'mobile':mobile}
        if request.method == 'POST':
          otp = request.POST.get('otp')
          profile = Profile.objects.filter(mobile=mobile).first()
        
          if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
           

            return redirect('home/')
          else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'login_otp.html' , context)
    
        return render(request,'login_otp.html' , context)
 
def send_otp(mobile,otp):
    
       
        url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{mobile}/{otp}'
        response = requests.get(url)
        return None
def register(request):  # sourcery skip: last-if-guard
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        img = request.FILES.get('image') 
        
        check_user = User.objects.filter(email = email).first()
        check_user_name=User.objects.filter(username = name).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile or check_user_name:
            context = {'message' : 'User already exists!please enter a unique username,email and mobile' , 'class' : 'danger' }
            return render(request,'register.html' , context)
            
        user = User(email = email , username = name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = user , mobile=mobile , otp = otp)
        
        if img:  # Save the image to the profile if an image was uploaded
            profile.image = img
        
        user_profile = UserProfileModel(user=user,name = name)
        profile.save()
        user_profile.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp') 
    return render(request,'register.html')
 
 
def otp(request):  # sourcery skip: extract-method, remove-unnecessary-else
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
                                
        if otp == profile.otp:
                       
            return redirect('home/')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)
            
        
    return render(request,'otp.html' , context)




def account_view(request, *args, **kwargs):
       # sourcery skip: extract-method, merge-dict-assign, move-assign
    context = {}
    user_id = kwargs.get("user_id")
    try:
        user1 = User.objects.get(pk=user_id)
        profile1 = Profile.objects.get(user=user1)  # Retrieve the Profile object
    except User.DoesNotExist:
        raise HttpResponse("User does not exist.")
    except Profile.DoesNotExist:
        raise HttpResponse("Profile does not exist.")
    if user1:
        context['id'] = user1.id
        context['username'] = user1.username
        context['profile_image'] = profile1.image.url
    
        try:
            friend_list = FriendList.objects.get(user=user1)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=user1)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends
            
            # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests =None
        user = request.user
        if user.is_authenticated and user != user1:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                
                if get_friend_request_or_false(sender=user1,receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=user1,receiver=user).id
                
                elif get_friend_request_or_false(sender=user1,receiver=user) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user,is_active=True)
            except :
                pass
        
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        context['request_sent']=request_sent
        context['friend_requests']=friend_requests
        return render(request, "accounts.html", context)

