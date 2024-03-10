from django.shortcuts import render , redirect

from D_project.models import Donation, Project
from .models import Profile
from .forms import SignupForm , UserForm , ProfileForm
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.



# def signup(request):
#     if request.method == 'POST':  ## save
#         form = SignupForm(request.POST)
#         if form.is_valid() :
#             form.save()
            
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             # login(request,user)
#             return redirect('login')

#     else: ## show form
#         form = SignupForm()
#     return render(request,'registration/signup.html',{'form':form})

def signup(request):
    if request.method == 'POST':  ## save
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            subject ='welcome to our web'
            message = f'Hi {username}, welcome to our website.'
            from_email = settings.EMAIL_HOST_USER
            recipients_list = [email]  
            send_mail(subject, message, from_email, recipients_list, fail_silently=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(username=username, password=password)
            
            login(request,user)
            return redirect('login')
    else: ## show form
        form = SignupForm()
    return render(request,'registration/signup.html',{'form':form})

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'/profile/profile.html',{'profile':profile})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    projects = Project.objects.filter(user=request.user)
    donations = Donation.objects.filter(user=request.user)

    if request.method == 'POST':
        userform = UserForm(request.POST , instance=request.user)
        profile_form = ProfileForm(request.POST ,request.FILES, instance=profile)
        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            # myform = profile_form.save(commit=False)
            # myform.user = request.user
            profile_form.save()
            return redirect('/')

    else:  
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request,'profile/profile_edit.html',{
        'userform' : userform , 
        'profileform' : profile_form ,
        'projects':projects,
        'donations': donations
        
        })

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')    



@login_required
def delete_account_view(request):
    if request.method == 'POST':
        # Verify user credentials (e.g., password confirmation)
        password = request.POST.get('password')
        user = request.user

        # Check if the entered password matches the user's password
        if user.check_password(password):
            # Delete the account
            user.delete()

            # Log out the user
            logout(request)
            return redirect('/')  # Redirect to the home page or a confirmation page
        else:
            # Password doesn't match, display an error message
            error_message = "Incorrect password. Please try again."

    else:
        error_message = None

    return render(request, 'registration/delete_account.html', {'error_message': error_message})

