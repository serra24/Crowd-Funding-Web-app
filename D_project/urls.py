from django.urls import path
from .views import projects, donate, project_details 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('<int:pk>/', project_details.as_view(), name="project_details"),
    path('', projects.as_view(), name='projects'),
    path('donate/<int:project_id>/', donate, name='donate'),

]