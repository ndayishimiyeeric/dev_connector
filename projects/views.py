from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects
from constants.utils import customPaginator


# Create your views here.

@login_required(login_url="login")
def projects(request):
    search_query, projects = searchProjects(request)
    # pagination
    page, custom_range, projects = customPaginator(request, projects, 5)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
        "page": page,
    }
    return render(request, "projects/projects.html", context)


@login_required(login_url="login")
def project(request, pk):
    obj = Project.objects.get(id=pk)
    tags = obj.tags.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = obj
        review.owner = request.user.profile
        review.save()
        var = obj.save_votes
        messages.success(request, f"successfully reviewed {obj}")
        return redirect('project', obj.id)

    context = {
        "project": obj,
        "tags": tags,
        "form": form,
    }
    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("dashboard")

    context = {
        "form": form,
        "page_title": "Add any project that you have worked on or you are working on.",
    }
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    context = {
        "form": form,
        "page_title": f"Update ({project.title})",
    }
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {
        "object": project,
    }
    return render(request, "delete_component.html", context)
