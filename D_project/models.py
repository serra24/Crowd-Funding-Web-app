from django.db import models

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
    name=models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    target = models.FloatField(default=100,null=True)
    tags = models.ManyToManyField(Tag)
    description=models.TextField(default="loream loream",max_length=800,null=True)
    start=models.DateTimeField(auto_now_add=True)
    end=models.DateTimeField()
    def __str__(self):
        return self.name

class Image(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    image = models.FileField(upload_to='projects/images',blank=True,null=True)
    
    
