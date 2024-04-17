from django.shortcuts import render
from D_project.models import *
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def home(req):
    theLatestimages=[]
    theTopimages=[]
    theFeaturedimages=[]
    category= Category.objects.all()
    for project in Project.GetLatestFiveProjects():
        print(project.tags)
        theLatestimages.append(Image.GetProjactImage(project))
    # print(images)
        for project in Project.GetTopFiveProjects():
            print(project.tags)
            theTopimages.append(Image.GetProjactImage(project))
    # print(images)
        for project in Project.GetFeaturedFiveProjects():
            print(project.tags)
            theFeaturedimages.append(Image.GetProjactImage(project))
    # print(images)
    theLatest = zip(Project.GetLatestFiveProjects(), theLatestimages)
    theTop=zip(Project.GetTopFiveProjects(), theTopimages)
    theFeatured=zip(Project.GetFeaturedFiveProjects(), theFeaturedimages)
    context={'theLatest':theLatest,'theTop':theTop,'theFeatured':theFeatured,'categories':category}

    return render(req,'home.html',context)

class MyListView(ListView):
    model = Donation
    template_name = 'home.html'
    context_object_name = 'donations'

class search(View):
    
    def get(self,req):
        return render(req,'search/search.html')
    def post(self,req):
        search_word=req.POST['search']
        # print (Project.GetProjectsByTag(search_word))
        # print(Project.GetProjectsByName(search_word))
        # project_result=Project.GetProjectsByTag(search_word)| Project.GetProjectsByName(search_word)
        project_result=set(list(Project.GetProjectsByTag(search_word))+list((Project.GetProjectsByName(search_word))))
        print(project_result)
        images=[]
        for project in project_result:
            images.append(Image.GetProjactImage(project))
        result= zip(project_result, images)
        context={'result':result}
        return render(req,'search/search.html',context)
    
        #     search_word=req.POST['search']
        # print (Project.GetProjectsByTag(search_word))
        # print(Project.GetProjectsByName(search_word))
        # # project_result=Project.GetProjectsByTag(search_word)+Project.GetProjectsByName(search_word)
        # project_result=Project.GetProjectsByTag(search_word)|Project.GetProjectsByName(search_word)
        # print(project_result)
        # images=[]
        # for project in Project.GetProjectsByName(search_word):
        #     images.append(Image.GetProjactImage(project))
        # result= zip(Project.GetProjectsByName(search_word), images)
        # context={'result':result}
    