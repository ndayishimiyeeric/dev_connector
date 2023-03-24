from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project, Review, Tag
from .forms import ProjectForm
from .utils import searchProjects, projectsPagination


# Create your views here.

@login_required(login_url="login")
def projects(request):
    search_query, projects = searchProjects(request)
    # pagination
    custom_range, projects = projectsPagination(request, projects, 5)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


@login_required(login_url="login")
def project(request, pk):
    obj = Project.objects.get(id=pk)
    tags = obj.tags.all()

    context = {
        "project": obj,
        "tags": tags,
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
