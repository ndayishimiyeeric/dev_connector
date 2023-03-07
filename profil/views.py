from django.shortcuts import render,redirect
from projects.models import *

from django.contrib.auth.decorators import login_required 

# Create your views here.

@login_required
def my_profil(request):
    return render(request,"my_profil.html",context={})


@login_required
def my_home_page(request):
    posts= Post.objects.select_related('user').all()
   
    context={
        "projects":posts,
    }
    
    return render(request,"my_home_page.html",context)