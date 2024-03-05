from django.shortcuts import render
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
# def projects(req):
#     return render(req,'D_project/projects.html')

class projects(ListView):
    model=Project
    template_name= 'D_project/projects.html'
    context_object_name = 'projects'