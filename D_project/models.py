from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
class Category(models.Model):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='categories/images',blank=True,null=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    tag=models.CharField(max_length=50)
    def __str__(self):
        return self.tag
   
class Project(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    target = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tags = models.ManyToManyField(Tag, related_name="projects")
    description = models.TextField(default="lorem ipsum", max_length=800, null=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def update_average_rating(self):
        total_ratings = Rating.objects.filter(project=self).aggregate(total=models.Sum('rating'))['total']
        num_ratings = Rating.objects.filter(project=self).count()
        if total_ratings is not None and num_ratings:
            self.average_rating = total_ratings / num_ratings
            self.save()
    @classmethod
    def GetLatestFiveProjects(self):
        return self.objects.all()[:5]
        # return self.objects.filter(name__in=(self.objects.all()[:5]))
        
    @classmethod
    def GetProjectsByName(self,name):
            return self.objects.filter(name__icontains=name)

    
    @classmethod
    def GetProjectsByTag(self,tag):
        try:
            return (Tag.objects.filter(tag=tag).first()).projects.all()
        except:
            return []


class Image(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    image = models.FileField(upload_to='projects/images',blank=True,null=True)

    
    @classmethod
    def GetProjactImage(self,projact):
        return f'/media/{self.objects.filter(project=projact).first().image}'



class Donation(models.Model):
    donation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)    


    def __self__(self):
        return self.donation



class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Rating for {self.project.name} by {self.user.username}"

class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)
    report_reason = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.name}'    

      
class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
from django.db import models
from django.contrib.auth import get_user_model
from .models import Comment

class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate content'),
        ('offensive', 'Offensive language'),
        ('other', 'Other'),
    ]

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    additional_comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on Comment {self.comment.id}"
         
class ReportProject(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate content'),
        ('offensive', 'Offensive language'),
        ('other', 'Other'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    additional_comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on Project {self.project.id}"


