from django.shortcuts import render

from account.models import Profile
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
from django.http import JsonResponse

def add_comment(request, project_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        project = Project.objects.get(id=project_id)
        comment = Comment.objects.create(user=request.user, project=project, text=text)
        # Return JSON response containing newly created comment data
        return JsonResponse({
            'comment': {
                'username': comment.user.username,
                'user_profile_image': comment.user.profile.image.url if comment.user.profile.image else 'https://maventricksdemo.co.in/bidonn/public/css/images/noImage.jpg',
                'text': comment.text,
            }
        })
    return JsonResponse({'error': 'Invalid Request'}, status=400)


