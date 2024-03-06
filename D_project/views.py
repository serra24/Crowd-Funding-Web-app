from django.shortcuts import render
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
def home(req):
    return render(req,'home.html')

class projects(ListView):
    model=Project
    template_name= 'D_project/projects.html'
    context_object_name = 'projects'

class project_details(DetailView):
    model=Project
    template_name=  'D_project/project_details.html'
    context_object_name=  'project'