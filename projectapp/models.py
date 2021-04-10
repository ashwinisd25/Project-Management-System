from django.db import models

STATUS_CHOICES = ( ('todo', 'TODO'),
            ('wip', 'WIP'),
            ('on_hold', 'ON_HOLD'),
            ('done', 'DONE') )

class Client(models.Model):
    name = models.CharField(max_length = 120, unique= True)
    email = models.EmailField()
    phone = models.IntegerField()
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length = 120, unique= True)
    description = models.TextField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    project_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @property
    def task_count(self):
        count = self.task_set.count()
        return count


class Task(models.Model):
    name = models.CharField(max_length = 120)
    description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES)
    
    def __str__(self):
        return self.name
