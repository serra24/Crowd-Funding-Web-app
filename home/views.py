from django.shortcuts import render
from D_project.models import *
# Create your views here.

def home(req):
    images=[]
    for project in Project.GetLatestFiveProjects():
        images.append(Image.GetProjactImage(project))
    print(images)
    theLatest = zip(Project.GetLatestFiveProjects(), images)
    context={'theLatest':theLatest}
    return render(req,'home.html',context)