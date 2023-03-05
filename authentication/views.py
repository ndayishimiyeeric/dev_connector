from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from authentication.forms import LoginForm,SingupUserForm
from django.conf import settings

# Create your views here.


def login_page(request):
    forms = LoginForm()
    message=''
    context={
        "erreur":False,
    }
    
    if request.method=="POST":
        forms = LoginForm(request.POST)
       
        email=request.POST.get('login')
        password=request.POST.get('password')
        print(email,password)
        #if forms.is_valid():
            #print(forms.cleaned_data['username'],forms.cleaned_data['password'])
        user =  authenticate(email=email,password=password)
        print("#######################=>",user)
        if user is not None:
            login(request,user)
            context['erreur'] = False
            #del context['login']
            #del context['mp']
            message = f'Bienvenue f{user.username}'
            return redirect("my_profil")
        else:
            context['erreur'] = True
            context['login'] = email
            context['mp'] = password
            context['message']="Login ou mot de passe incorrect"

    return render(request,"authenticate/login.html",context)


def register(request):
    forms=SingupUserForm()
    if request.method=="POST":
        forms = SingupUserForm(request.POST)
       
        if forms.is_valid():
            user= forms.save()
            login(request,user)
            return redirect("my_profil")
        


    return render(request,'authenticate/registerUser.html',context={"forms":forms})


def logout_user(request):
    logout(request)
    return redirect('authentication')

