from django.contrib import admin
from .models import Profile, Skill, Experience, Education, Follower, News
# Register your models here.

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Follower)
admin.site.register(News)
