from django.contrib import admin
from .models import Profile, Skill, Experience, Education, Message, Follower
# Register your models here.

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Message)
admin.site.register(Follower)
