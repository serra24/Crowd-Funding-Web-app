from django.shortcuts import redirect, render

from account.models import Profile
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout

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
def profile(request):
    user = Profile.objects.get(user=user.id)
    return render(request, 'D_project/project_details.html',{'user':user})

@login_required
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

class delete_project(LoginRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    model = Project
    template_name = 'D_project/delete.html'
    success_url = reverse_lazy('projects')

