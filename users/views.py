from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomerUserCreationForm, ProfileForm

# Create your views here.

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is incorrect")

    context = {
        'page': page
    }
    return render(request, 'users/login_register.html', context)

def userRegister(request):

    if request.user.is_authenticated:
        return redirect('profiles')
    
    form = CustomerUserCreationForm()
    page = 'register'
    
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = user.username.lower()
            user.save()

            messages.success(request, "Registered successfully, Welcome" + username + "😁")
            login(request, user)

            return redirect('edit-profile')
        else:
            messages.error(request, "An error has occured during registration.")

    context = {
        'form': form,
        'page': page
    }

    return render(request, 'users/login_register.html', context)

def userLogout(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('welcome')

def userWelcome(request):
    return render(request, 'users/welcome.html')

@login_required(login_url='login')
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)

@login_required(login_url='login')
def profile(request, pk):
    obj = Profile.objects.get(id=pk)
    mainSkills = obj.skill_set.exclude(description__exact="")
    otherSkills = obj.skill_set.filter(description__exact="")

    experiences = obj.experience_set.all().order_by('-is_current', '-to_date')

    educations = obj.education_set.all().order_by('-is_current', '-to_date')
    context = {
        'profile': obj,
        'mainSkills': mainSkills,
        'otherSkills': otherSkills,
        'experiences': experiences,
        'educations': educations
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def userDashboard(request):
    profile = request.user.profile
    userProjects = profile.project_set.all()
    userExperiences = profile.experience_set.all().order_by('-is_current', '-to_date')
    userEducations = profile.education_set.all().order_by('-is_current', '-to_date')
    userSkills = profile.skill_set.all()
    context = {
        'profile': profile,
        'userProjects': userProjects,
        'userExperiences': userExperiences,
        'userEducations': userEducations,
        'userSkills': userSkills
    }
    return render(request, 'users/dashboard.html', context)

@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'users/profile_form.html', context)
