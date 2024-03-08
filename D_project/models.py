from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.

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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,default=1)
    name=models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    target = models.FloatField(default=100,null=True)
    tags = models.ManyToManyField(Tag)
    description=models.TextField(default="loream loream",max_length=800,null=True)
    start=models.DateTimeField(auto_now_add=True)
    end=models.DateTimeField()
    def __str__(self):
        return self.name
    @classmethod
    def GetLatestFiveProjects(self):
        return self.objects.all()[:5]
        # return self.objects.filter(name__in=(self.objects.all()[:5]))
        
    @classmethod
    def GetProjectsByName(self,name):
        return self.objects.filter(name__icontains=name)
    
    # @classmethod
    # def GetProjectsByTag(self,tag):
    #     return self.objects.filter(tags__icontains=tag)

class Image(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    image = models.FileField(upload_to='projects/images',blank=True,null=True)

    @classmethod
    def GetProjactImage(self,projact):
        return f'/media/{self.objects.filter(project=projact).first().image}'
        
    
class Donation(models.Model):
    donation = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(Register, on_delete=models.CASCADE)    


    def __self__(self):
        return self.donation



class Rate(models.Model):
    rating = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    # user = models.ForeignKey(Register, on_delete=models.CASCADE)    


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.name}'    

    def __str__(self):
        return str(self.rating)    

class Donation(models.Model):
    donation = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(Register, on_delete=models.CASCADE)    


    def __self__(self):
        return self.donation



class Rate(models.Model):
    rating = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    # user = models.ForeignKey(Register, on_delete=models.CASCADE)    


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.name}'    

    def __str__(self):
        return str(self.rating)    
