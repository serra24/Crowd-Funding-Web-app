 
from django.shortcuts import redirect, render
  
from django.shortcuts import render, redirect , get_object_or_404
  

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

  
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.db.models import Avg
from .models import Project, Donation, Rate
  
# Create your views here.

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

 
  

def donate(request, project_id):
    project = Project.objects.get(id=project_id)
    total_donation = Donation.objects.filter(project=project).aggregate(Sum('donation'))['donation__sum'] or 0
    remaining_amount = max(project.target - total_donation, 0)
       
       
    if request.method == 'POST':
        if 'donate_amount' in request.POST:
            donate_amount = float(request.POST.get('donate_amount'))
            if remaining_amount > 0 and donate_amount > 0:
                # Create a new donation
                donation = Donation.objects.create(project=project, donation=donate_amount)
                # Deduct the donated amount from the total budget
                total_bug =project.target
                total_bug -= donate_amount
                remaining_amount =total_bug 
                project.save()
                return redirect('projects')  # Redirect to a success page after donation
            else:
                # Redirect back to the donation page with an error message
                return redirect('donate', project_id=project.id)
        
    
    return render(request, 'D_project/donation.html', {'project': project, 'total_donation': total_donation, 'remaining_amount': remaining_amount,})


# def rate_project(request, project_id):
#     if request.method == 'POST':
#         project = Project.objects.get(pk=project_id)
#         rating = int(request.POST.get('rating'))
#         # Assuming user is authenticated and rating is between 1 and 5
#         project.ratings.create(user=request.user, rating=rating)
#         return redirect('project', project_id=project_id)
    
   
   
def handle_rating_submission(request, project_id, rating):
    project = get_object_or_404(Project, pk=project_id)
    
    # Create a new Rate object
    rate = Rate.objects.create(rating=rating, project=project)

    # Update the average rating for the project
    project.rate = calculate_average_rating(project)
    project.save()

    # Retrieve the average rating for the project
    average_rating = project.rate

    # Retrieve the latest rating for the project
    latest_rating = rate.rating
    # Handle the rest of your response or redirect as needed
    return render(request, 'D_project/donation.html',  {'average_rating': average_rating, 'latest_rating': latest_rating})

def calculate_average_rating(project):
    average_rating = Rate.objects.filter(project=project).aggregate(Avg('rating'))['rating__avg']

    if average_rating is not None:
        return round(average_rating, 2)
    else:
        return 0       

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


  
