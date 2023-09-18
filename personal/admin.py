from django.contrib import admin
from personal.models import ChatModel,UserProfileModel
# Register your models here.


@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id','sender','message','thread_name','timestamp']
    
@admin.register(UserProfileModel)
class UserProfileModelAdmin(admin.ModelAdmin):
  list_display = ['id','user','name','online_status']
