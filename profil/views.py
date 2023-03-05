from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required 

# Create your views here.

@login_required
def my_profil(request):
    return render(request,"my_profil.html",context={})