from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Tags)
admin.site.register(Donation)
admin.site.register(Rate)