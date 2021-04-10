from django import forms
from . models import Project, Task

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = ['name', 'description','client',]


  
    widgets = {
            'name': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Name'
                }
            ),
            'description': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Description'
                }
            ),
            'client': forms.Select(attrs=
            {'class': 'form-control'}
               
            ),
            

    }

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['name', 'description','project','status']
    exclude = ('project',)
    widgets = {
            'name': forms.TextInput(attrs={
                    'class': 'form-control',
                }
            ),
             'description': forms.Textarea(attrs={
                    'class': 'form-control',
                }
            ),
            'status': forms.Select(attrs={
                'class': 'form-control',
                }
            ),
        }