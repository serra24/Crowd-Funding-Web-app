from django.urls import path
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('<int:pk>/',project_details.as_view(),name="project_details"),
    path('',projects.as_view(),name='projects'),
    path('createProject',create_project,name="createProject")
]