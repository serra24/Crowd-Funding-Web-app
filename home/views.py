from django.shortcuts import render
from D_project.models import *
from django.views import View
# Create your views here.

def home(req):
    images=[]
    for project in Project.GetLatestFiveProjects():
        print(project.tags)
        images.append(Image.GetProjactImage(project))
    print(images)
    theLatest = zip(Project.GetLatestFiveProjects(), images)
    context={'theLatest':theLatest}
    return render(req,'home.html',context)



class search(View):
    
    def get(self,req):
        return render(req,'search/search.html')
    def post(self,req):
        search_word=req.POST['search']
        print(Project.GetProjectsByName(search_word))
        images=[]
        for project in Project.GetProjectsByName(search_word):
            images.append(Image.GetProjactImage(project))
        result= zip(Project.GetProjectsByName(search_word), images)
        context={'result':result}
        return render(req,'search/search.html',context)
    