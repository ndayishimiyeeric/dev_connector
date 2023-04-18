from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Follower, Skill, Experience, Education, News
from .forms import CustomerUserCreationForm, ProfileForm, SkillForm, ExperienceForm, EducationForm, FollowForm
from .utils import searchProfiles, searchUserProjects
from constants.utils import customPaginator


# Create your views here.

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'feed')
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
    messages.warning(request, "You have been logged out!")
    return redirect('register')


def userWelcome(request):
    return render(request, 'users/welcome.html')


@login_required(login_url='login')
def profiles(request):
    search_query, profiles = searchProfiles(request)
    query, userProjects = searchUserProjects(request)
    # pagination
    page, custom_range, profiles, count = customPaginator(request, profiles, 3)
    news = News.objects.all().order_by('-created_at')[:3]

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'count': count,
        'userProjects': userProjects,
        'query': query,
        'news': news,
    }
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    obj = Profile.objects.get(id=pk)
    mainSkills = obj.skill_set.exclude(description__exact="")
    otherSkills = obj.skill_set.filter(description__exact="")
    userProjects = obj.project_set.all()
    # pagination
    page, custom_range, userProjects, count = customPaginator(request, userProjects, 3)

    # top 3 projects by votes_count
    topProjects = obj.project_set.all().order_by('-votes_count')[:3]

    experiences = obj.experience_set.all().order_by('-is_current', '-to_date')

    educations = obj.education_set.all().order_by('-is_current', '-to_date')

    # get followers and following
    following = obj.following.all()
    followers = obj.followers.all()
    formFollow = FollowForm()

    context = {
        'profile': obj,
        'mainSkills': mainSkills,
        'otherSkills': otherSkills,
        'experiences': experiences,
        'educations': educations,
        'userProjects': userProjects,
        'custom_range': custom_range,
        'count': count,
        'topProjects': topProjects,
        'followers': followers,
        'following': following,
        'formFollow': formFollow
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
            return redirect('user-profile', pk=profile.id)

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
            return redirect('user-profile', pk=profile.id)

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
            return redirect('user-profile', pk=profile.id)

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
        return redirect('user-profile', pk=profile.id)
    context = {
        "object": skill,
    }
    return render(request, "delete_component.html", context)


@login_required(login_url='login')
def addExperience(request):
    profile = request.user.profile
    form = ExperienceForm()
    default_url = '/profile/' + str(request.user.profile.id)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.owner = profile
            experience.save()
            messages.success(request, "Experience created successfully")
            return redirect('edit-profile', pk=profile.id)
        else:
            messages.error(request, "An error has occurred during experience creation 😔 try again")

    context = {
        'profile': profile,
        'form': form,
        'text': ' Add any developer/programming position that you have had in the past',
        'page': 'Add',
        'default_url': default_url,
    }

    return render(request, 'users/experience_form.html', context)


@login_required(login_url='login')
def updateExperience(request, pk):
    profile = request.user.profile
    experience = profile.experience_set.get(id=pk)
    form = ExperienceForm(instance=experience)
    default_url = '/profile/' + str(request.user.profile.id)

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
        'default_url': default_url,
    }
    return render(request, 'users/experience_form.html', context)


@login_required(login_url='login')
def deleteExperience(request, pk):
    profile = request.user.profile
    experience = profile.experience_set.get(id=pk)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully")
        return redirect('edit-profile', pk=profile.id)

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
            return redirect("edit-profile", pk=profile.id)
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
            return redirect("user-profile", pk=profile.id)
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
        return redirect('user-profile', pk=profile.id)

    context = {
        'object': education,
    }
    return render(request, 'delete_component.html', context)


# followers views

@login_required(login_url='login')
def follow(request, pk):
    receiver_profile = get_object_or_404(Profile, id=pk)

    # check if the user is already following the receiver
    if request.user.profile in receiver_profile.followers.all():
        messages.error(request, f"You are already following {receiver_profile}")
        return redirect(request.GET['next'] if 'next' in request.GET else 'user-profile', pk=pk)
    # check if the user is trying to follow himself
    if request.user.profile == receiver_profile:
        messages.error(request, "You can't follow yourself")
        return redirect(request.GET['next'] if 'next' in request.GET else 'user-profile', pk=pk)

    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            new_follow = form.save(commit=False)
            new_follow.sender_profile = request.user.profile
            new_follow.receiver_profile = receiver_profile
            new_follow.save()
            messages.success(request, f"You are now following {new_follow.receiver_profile}")
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-profile', pk=pk)
        else:
            messages.error(request, f"Can't follow {receiver_profile}")
    return redirect('user-profile', pk=pk)


@login_required(login_url='login')
def unfollow(request, pk):
    follower = get_object_or_404(Follower, sender_profile=request.user.profile, receiver_profile_id=pk)
    follower.delete()
    messages.success(request, f"You are no longer following {follower.receiver_profile}")
    return redirect(request.GET['next'] if 'next' in request.GET else 'user-profile', pk=pk)


@login_required(login_url='login')
def feed(request):
    user_profile = request.user.profile
    feed_items = user_profile.feed_items()
    form = FollowForm()
    news = News.objects.all()

    query, userProjects = searchUserProjects(request)

    context = {
        'feed_items': feed_items,
        'userProjects': userProjects,
        'query': query,
        'form': form,
        'news': news,
    }

    return render(request, 'users/feed.html', context)



