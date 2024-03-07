from django.shortcuts import render
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages

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

def create_project(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            for i in files:
                Image.objects.create(project=f, image=i)
            messages.success(request, "New Project Added")
            return HttpResponseRedirect("projects/")
        else:
            print(form.errors)
    else:
        form = ProjectForm()
        imageform = ImageForm()

    return render(request, "D_project/create_project.html", {"form": form, "imageform": imageform})    