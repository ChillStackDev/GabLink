from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from friend.models import FriendList, FriendRequest
from personal.models import ChatModel

# Create your views here.
from django.http import HttpResponse


@login_required(login_url='/') 
def home(request):
      try:
        profile = Profile.objects.get(user=request.user)
        try:
            friend_list = FriendList.objects.get(user=request.user)
            friends = friend_list.friends.all()
        except FriendList.DoesNotExist:
            friends = []  # Create an empty list of friends when FriendList doesn't exist
        return render(request, 'home.html', {'profile': profile, 'friends': friends})
      except Profile.DoesNotExist:
        return HttpResponse("Your profile does not exist.")

def chatPage(request,username):
     try:
        user_obj = User.objects.get(username=username) 
        profile = Profile.objects.get(user=request.user)
        friend_list = FriendList.objects.get(user=request.user)
        friends = friend_list.friends.all()
        
        if request.user.id > user_obj.id:
            thread_name = f'chat_{request.user.id}-{user_obj.id}'
        else:
          thread_name = f'chat_{user_obj.id}-{request.user.id}'
    
        message_obj  = ChatModel.objects.filter(thread_name=thread_name)
        return render(request, 'main_chat.html', {'profile': profile, 'friends': friends , 'user':user_obj ,'messages':message_obj})
     except Profile.DoesNotExist:
        return HttpResponse("Your profile does not exist.")
     except FriendList.DoesNotExist:
        return HttpResponse("Your friend list does not exist.")


     
def account_search_view(request, *args, **kwargs):
      # sourcery skip: for-append-to-extend
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = User.objects.filter(username__icontains=search_query)
            user = request.user
            accounts = []  # [(account1, True), (account2, False), ...]
            
            if user.is_authenticated:
                try:
                    auth_user_friend_list = FriendList.objects.get(user=user)
                    for account in search_results:
                        accounts.append((account, auth_user_friend_list.is_mutual_friends(account)))
                    context['accounts'] = accounts
                except FriendList.DoesNotExist:
                    for account in search_results:
                        accounts.append((account, False))
                    context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts

    return render(request, "search.html", context)



