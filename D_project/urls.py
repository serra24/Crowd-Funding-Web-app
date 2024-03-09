from django.urls import path
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('<int:project_id>/',project_details,name="project_details"),
    path('',projects.as_view(),name='projects'),
    path('createProject',create_project,name="createProject"),
    path('deleteProject/<int:project_id>/',delete_project,name="deleteProject"),
    path('project/<int:project_id>/add_comment/', add_comment, name='add_comment'), 
    path('project/<int:project_id>/donate/', donate, name='donate'),
    path('donate/success/', donate_success, name='donate_success'),
    path('<int:comment_id>/add_reply/', add_reply, name='add_reply'),
    path('comment/<int:comment_id>/report/', report_comment, name='report_comment'),
    path('project/<int:project_id>/report/', report_project, name='report_project'),

]
