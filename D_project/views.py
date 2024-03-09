
from django.shortcuts import render, redirect , get_object_or_404, redirect , get_object_or_404
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse  
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

def featured_projects(request):
    featured_projects = Project.objects.filter(is_featured=True)
    return render(request, 'home.html', {'featured_projects': featured_projects})

# class project_details(DetailView):
#     model=Project
#     template_name=  'D_project/project_details.html'
#     context_object_name=  'project'

def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    donations = Donation.objects.filter(project=project)
    context = {
        'project': project,
        'donations': donations,
        'remain': project.target - project.current_amount
    }
    return render(request, 'D_project/project_details.html', context)

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
            return HttpResponseRedirect("/")
        else:
            print(form.errors)
    else:
        form = ProjectForm()
        imageform = ImageForm()

    return render(request, "D_project/create_project.html", {"form": form, "imageform": imageform})    

# class delete_project(LoginRequiredMixin,DeleteView):
#     login_url = '/accounts/login/'
#     model = Project
#     template_name = 'D_project/delete.html'
#     success_url = reverse_lazy('projects')
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    donation = Donation.objects.filter(project=project)
    # Calculate the total donation amount for the project
    total_donation_amount = Donation.objects.filter(project=project).aggregate(total=models.Sum('donation'))['total']
    if  total_donation_amount and total_donation_amount > float(project.target) * 0.25:
        # messages.error(request, "Cannot delete the project. Total donations exceed 25% of the target amount.")
        return render(request,'D_project/project_details.html', {'msg':'Cannot delete the project,Total donations exceed 25% of the target amount.','project':project,'donation':donation})
    else:
        if request.method == 'POST':
        # Confirmation code
            confirm = request.POST.get('confirm', False)
            if confirm:
                project.delete()
                # messages.success(request, "The project has been deleted successfully.")
                return redirect('projects')
            else:
                # messages.error(request, "Project deletion canceled.")
                return redirect('project_details', project_id=project_id)

            # messages.success(request, "The project has been deleted successfully.")
        return render(request,'D_project/delete.html', {'msg':'','project':project,'donation':donation})
        
@login_required
def donate(request, project_id):
    project = Project.objects.get(id=project_id)
    # total_donation = Donation.objects.filter(project=project).aggregate(Sum('donation'))['donation__sum'] or 0
    # remaining_amount = max(project.target - total_donation, 0)
       
       
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['donation']
            # You can perform additional validation and payment processing here
            donation = Donation.objects.create(project=project,user=request.user, donation=amount)
            project.current_amount += amount
            project.save()
            return redirect('/')
    else:
        form = DonationForm()

    context = {
        'project': project,
        'form': form,
        'remain': project.target - project.current_amount
    }
    return render(request, 'D_project/donation.html', context)

def donate_success(request):
    return render(request, 'D_project/project_details.html')


# def rate_project(request, project_id):
#     if request.method == 'POST':
#         project = Project.objects.get(pk=project_id)
#         rating = int(request.POST.get('rating'))
#         # Assuming user is authenticated and rating is between 1 and 5
#         project.ratings.create(user=request.user, rating=rating)
#         return redirect('project', project_id=project_id)
    
   
@login_required   
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



@login_required
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
@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        if reply_text:
            comment = get_object_or_404(Comment, id=comment_id)
            reply = Reply.objects.create(user=request.user, comment=comment, reply_text=reply_text)
            response_data = {
                'reply': {
                    'username': reply.user.username,
                    'user_profile_image': reply.user.profile.image.url if reply.user.profile.image else 'https://maventricksdemo.co.in/bidonn/public/css/images/noImage.jpg',
                    'reply_text': reply.reply_text,
                    'created_at': reply.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Reply text is empty'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400) 
        

from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import ReportForm
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    reports = Report.objects.filter(comment=comment)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            report = Report.objects.create(comment=comment, user=request.user, reason=reason)
            comment.reported = True
            comment.report_reason = reason
            comment.save()
            return render(request, 'D_project/succ_report.html')
    else:
        form = ReportForm()
    return render(request, 'D_project/reoprtcomment.html', {'form': form, 'reports': reports})
    

def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            project_report = ReportProject.objects.create(
                project=project,
                user=request.user,
                reason=reason
            )
            project.reported = True
            project.save()
            return render(request, 'D_project/succ_report.html')
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ReportForm()

    return render(request, 'D_project/report_project.html', {'form': form, 'project': project})

