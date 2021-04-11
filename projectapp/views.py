from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView, DetailView
from .forms import ProjectForm, TaskForm
from .models import Project, Task,Client
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic.edit import DeleteView,UpdateView

# update project status automatically when new task created or edited.
def ProjectStatus(project_id):
    project= Project.objects.get(pk=project_id)
    task = Task.objects.filter(project_id=project_id)
    for i in task:
        if i.status !="done":
            project.end_date = None
            project.project_status = False
        else :
            project.end_date = datetime.now()
            project.project_status = True
    return project

def home(request):
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
            return render(request,"projects/create_task.html", {"form":form})
    return render(request, 'projects/projectdetail.html', context)

def CreateTask(request, project_id):
    template_name = 'projects/create_task.html'
    project= Project.objects.get(pk=project_id)
    form_class = TaskForm
    return render(request,template_name, {'form':form_class, 'project': project})

def TaskList(request,project_id):
    tasks = Task.objects.filter(project=project_id)
    return render(request, 'projects/tasklist.html', {'tasks':tasks, "project_id" : project_id})
    
def TaskEdit(request,task_id):
    task_obj = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_obj.name=form.cleaned_data.get('name')
            task_obj.description = form.cleaned_data.get('description')
            task_obj.status = form.cleaned_data.get('status')
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
    task.delete()
    return redirect(request.META['HTTP_REFERER'])
    
