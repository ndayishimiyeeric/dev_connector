from django.shortcuts import render, redirect
from .models import Project, Review, Tag
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, "projects/projects.html", context)

def project(request, pk):
    obj = Project.objects.get(id=pk)
    tags = obj.tags.all()

    context = {
        "project": obj,
        "tags": tags,
    }
    return render(request, "projects/single-project.html", context)

def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {
        "form": form,
        "page_title": "Add any project that you have worked on or you are working on.",
    }
    return render(request, "projects/project_form.html", context)

def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {
        "form": form,
        "page_title": f"Update {project.title}",
    }
    return render(request, "projects/project_form.html", context)

def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {
        "object": project,
    }
    return render(request, "projects/delete_component.html", context)
