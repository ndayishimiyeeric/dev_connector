from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ProjectSerializer
from projects.models import Project


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': '/api/products'},
    ]
    return Response(routes)


@api_view(['GET'])
def get_products(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
