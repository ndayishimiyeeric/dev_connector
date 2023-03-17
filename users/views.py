from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomerUserCreationForm, ProfileForm, SkillForm, ExperienceForm, EducationForm


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

            messages.success(request, "Registered successfully, Welcome " + username + "😁")
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


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created successfully")
            return redirect('dashboard')

    context = {
        'profile': profile,
        'form': form,
        'text': 'Create a new skill',
        'page': 'Create'
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully")
            return redirect('dashboard')

    context = {
        'profile': profile,
        'form': form,
        'text': f'Update skill ({skill.name})',
        'page': 'update',
        'skill': skill,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect('dashboard')
    context = {
        "object": skill,
    }
    return render(request, "delete_component.html", context)


@login_required(login_url='login')
def addExperience(request):
    profile = request.user.profile
    form = ExperienceForm()

    if request.method == 'POST':
        form = ExperienceForm(request.POST)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.owner = profile
            experience.save()
            messages.success(request, "Experience created successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "An error has occurred during experience creation 😔 try again")

    context = {
        'profile': profile,
        'form': form,
        'text': ' Add any developer/programming position that you have had in the past',
        'page': 'Add'
    }

    return render(request, 'users/experience_form.html', context)


@login_required(login_url='login')
def updateExperience(request, pk):
    profile = request.user.profile
    experience = profile.experience_set.get(id=pk)
    form = ExperienceForm(instance=experience)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "An error has occurred during experience update 😔 try again")

    context = {
        'profile': profile,
        'form': form,
        'text': f' Update experience ({experience.title})',
        'page': 'update',
        'experience': experience,
    }
    return render(request, 'users/experience_form.html', context)


@login_required(login_url='login')
def deleteExperience(request, pk):
    profile = request.user.profile
    experience = profile.experience_set.get(id=pk)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully")
        return redirect('dashboard')

    context = {
        "object": experience,
    }

    return render(request, "delete_component.html", context)


@login_required(login_url='login')
def addEducation(request):
    profile = request.user.profile
    form = EducationForm()

    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.owner = profile
            education.save()
            messages.success(request, "Education created successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "An error has occurred during education creation 😔 try again")
    context = {
        'profile': profile,
        'form': form,
        'text': ' Add any school, bootcamp, etc that you have attended',
        'page': 'Add'
    }
    return render(request, "users/education_form.html", context)


@login_required(login_url='login')
def updateEducation(request, pk):
    profile = request.user.profile
    education = profile.education_set.get(id=pk)
    form = EducationForm(instance=education)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)

        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "An error has occurred during education update 😔 try again")

    context = {
        'form': form,
        'text': f' Update education ({education})',
        'page': 'update',
        'profile': profile,
        'education': education
    }

    return render(request, 'users/education_form.html', context)


@login_required(login_url='login')
def deleteEducation(request, pk):
    profile = request.user.profile
    education = profile.education_set.get(id=pk)

    if request.method == 'POST':
        education.delete()
        messages.success(request, "Education deleted successfully")
        return redirect('dashboard')

    context = {
        'object': education,
    }
    return render(request, 'delete_component.html', context)
