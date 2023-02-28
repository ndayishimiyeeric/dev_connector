from django.shortcuts import render

# Create your views here.

projectsList = [
    {
        "id": 1,
        "title": "Project 1",
        "description": "This is project 1",
    },
    {
        "id": 2,
        "title": "Project 2",
        "description": "This is project 2",
    },
    {
        "id": 3,
        "title": "Project 3",
        "description": "This is project 3",
    },
]

def projects(request):
    text = "This is the projects page"
    return render(request, "projects/projects.html", {"text": text, "projects": projectsList})

def project(request, pk):
    obj = None
    for project in projectsList:
        if project["id"] == pk:
            obj = project
            break
    return render(request, "projects/single-project.html", {"project": obj})
