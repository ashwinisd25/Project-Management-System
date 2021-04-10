from django.urls import path
from projectapp import views

urlpatterns = [
    path('create/', views.CreateProjectView.as_view(), name='createproject'),
    path('createtask/<int:project_id>', views.CreateTask, name='createtask'),
    path('list/', views.ProjectListView.as_view(), name='projectlist'),
    path('delete/<int:project_id>', views.ProjectDeleteView, name='projectdelete'),
    path('<int:project_id>/', views.ProjectDetail, name='projectdetailview'),
    path('<int:project_id>/tasklist', views.TaskList, name='tasklist'),
    path('edittask/<int:task_id>', views.TaskEdit, name='edittask'),
    path('deletetask/<int:task_id>', views.TaskDelete, name='deletetask'),
    path('ongoing/', views.OngoingProject, name='ongoingproject'),

]
