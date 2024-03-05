from django.urls import path
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',projects,name="projects"),
    path('',projects.as_view(),name='projects')
]