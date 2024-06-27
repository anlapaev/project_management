from django import forms
from .models import Project, Task, Comment
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'manager', 'members']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'members': forms.CheckboxSelectMultiple,
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority', 'project', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(members=user)
            self.fields['assigned_to'].queryset = User.objects.filter(projects__in=self.fields['project'].queryset).distinct()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
