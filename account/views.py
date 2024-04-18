from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render , redirect

from D_project.models import Donation, Project
from .models import Profile
from .forms import SignupForm , UserForm , ProfileForm
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

from django.contrib.auth import get_user_model
from django.contrib import messages  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()
            if (form.errors):
                messages.error(request, "message")  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('registration/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm() 

    return render(request, 'registration/signup.html', {'form': form})  


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')
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

