from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class Project(models.Model):
    name=models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    target = models.FloatField(default=100,null=True)
    description=models.TextField(default="loream loream",max_length=800,null=True)
    start=models.DateTimeField(auto_now_add=True)
    end=models.DateTimeField()
    remaining_amount=models.FloatField(default=100,null=True)
    def __str__(self):
        return self.name

class Image(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/images',blank=True,null=True)
    
    
class Tags(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    tag=models.CharField(max_length=50)
    def __str__(self):
        return self.tag
    

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
    
    def __str__(self):
        return str(self.rating)
   
    # rating = models.IntegerField(validators=[MaxValueValidator(5)])    