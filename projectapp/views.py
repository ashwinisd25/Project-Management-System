from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView, DetailView
from .forms import ProjectForm, TaskForm
from .models import Project, Task,Client
from django.urls import reverse_lazy
from datetime import datetime

# update project status automatically when new task created or edited.
def ProjectStatus(project_id):
    project= Project.objects.get(pk=project_id)
    for i in project.task_set.all():
        if i.status !="done":
            project.project_status = False
            break
        project.project_status = True
    if project.project_status == True:
        project.end_date = datetime.now()
    project.end_date = None
    return project

def home(request):
    project= Project.objects.all()
    for i in project:
        for y in i.task_set.all():
            print(y.status) 
        print(i.task_set.all())
    

    return render(request, 'projects/home.html')

def client(request):
    clients= Client.objects.all()
    return render(request, 'projects/clients.html',{'clients': clients})


class CreateProjectView(CreateView):
    template_name = 'projects/create_project.html'
    model = Project  
    form_class = ProjectForm

class ProjectListView(ListView):
    template_name = 'projects/projectlist.html'
    form_class = ProjectForm
    queryset = Project.objects.all()
    context_object_name = 'project_list'
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        queryset = Project.objects.all()
        if form.is_valid():
            form.save()
            return render(request,self.template_name, {"project_list":queryset})
        else:
            return render(request,"projects/create_project.html", {"form":form})

# returns the project list which are on going or incomplete to template
def OngoingProject(request):
    template_name = 'projects/ongoing_projects.html'
    project = Project.objects.filter(project_status=False)     
    return render(request, template_name,{"ongoing_project": project} )

def ProjectDeleteView(request, project_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
        except:
            return redirect('projectlist')
    return redirect('projectlist')

# task creation is handelled in this view in POST part.
def ProjectDetail(request, project_id):
    task = Task.objects.filter(project=project_id)
    project = Project.objects.get(pk=project_id)
    context={
            'project':project,
            'task':task
        }
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            newtask = Task()
            name= form.cleaned_data['name']
            description= form.cleaned_data["description"]
            project=Project.objects.get(pk=project_id)
            status= form.cleaned_data['status']
            newtask=Task(name=name ,description= description, project=project,status=status)
            newtask.save()
            p = ProjectStatus(project_id) 
            p.save()
            return redirect('projectdetailview', project_id)
        else:
            return render(request,"projects/create_task.html", {"form":form,"project":project })
    return render(request, 'projects/projectdetail.html', context)

def CreateTask(request, project_id):
    template_name = 'projects/create_task.html'
    project= Project.objects.get(pk=project_id)
    form_class = TaskForm
    return render(request,template_name, {'form':form_class, 'project': project})

def TaskList(request,project_id):
    tasks = Task.objects.filter(project=project_id)
    return render(request, 'projects/tasklist.html', {'tasks':tasks, "project_id" : project_id})
    
#  Task status can be edited.
#  the existing task object is saved in variable and updated with new status.
def TaskEdit(request,task_id):
    task_obj = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        if request.POST.get("status"):
            task_obj.status = request.POST.get("status")
            task_obj.save()
            p = ProjectStatus(task_obj.project_id)
            p.save()         
            return redirect('tasklist',task_obj.project.pk)
        else:
            return render(request,"projects/taskedit.html", {"form":form})
    template_name = 'projects/taskedit.html'
    form = TaskForm(initial={'name': task_obj.name,'description': task_obj.description,'status':task_obj.status })
    context = {'form': form, 'task_obj': task_obj}
    return render(request, template_name, context)

def TaskDelete(request,task_id):
    task = Task.objects.get(pk=task_id)
    p = ProjectStatus(task.project_id)
    p.save()
    task.delete()
    return redirect(request.META['HTTP_REFERER'])
    
