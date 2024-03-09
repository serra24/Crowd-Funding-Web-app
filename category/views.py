from django.shortcuts import render
from D_project.models import Category
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
class categories(ListView):
    model=Category
    template_name= 'category/categories.html'
    context_object_name = 'categories'

class category(ListView):
    model=Category
    template_name= 'base.html'
    context_object_name = 'categories'
