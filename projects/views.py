from django.shortcuts import render
import datetime
from projects.models import Project,Post,Comment,Like

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
    projects= Project.objects.select_related('user').all()
    for i in projects:
        print(i)
   
    return render(request, "projects/projects.html",context={"projects":projects})

def project(request, pk):
    obj = None
    for project in projectsList:
        if project["id"] == pk:
            obj = project
            break
    return render(request, "projects/single-project.html", {"project": obj})


def addPost(request):

    if request.method=="POST":
        image=None
        if request.FILES:
            image = request.FILES['image']
        project= Post.objects.create(
                         description = request.POST.get('description'),
                         user=request.user,
                         image=image
                         )
        
    return render(request,"projects/AddPost.html")



def addProject(request):

    if request.method=="POST":
        image=None
        if request.FILES:
            image = request.FILES['image']
        project= Project.objects.create(title=request.POST.get("title"),
                         description = request.POST.get('description'),
                         source_code= request.POST.get('code'),
                         live_preview=request.POST.get('live'),
                         created_at=datetime.datetime.now(),
                         user_id=request.user,
                         image=image
                        
                         )
        
    return render(request,"projects/AddProject.html")
