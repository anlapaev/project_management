from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import User

@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.members.add(request.user)
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def project_add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        project.members.add(user)
        return redirect('project_detail', pk=pk)
    users = User.objects.exclude(id__in=project.members.all())
    return render(request, 'projects/project_add_member.html', {'project': project, 'users': users})

@login_required
def project_remove_member(request, project_pk, user_pk):
    project = get_object_or_404(Project, pk=project_pk)
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        project.members.remove(user)
        return redirect('project_detail', pk=project_pk)
    return render(request, 'projects/project_confirm_remove_member.html', {'project': project, 'user': user})

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(user=request.user)
    return render(request, 'projects/task_form.html', {'form': form, 'project': project})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project  # Получаем проект из задачи
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.pk)  # Используем task.project.pk
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'projects/task_form.html', {'form': form, 'task': task, 'project': project})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', pk=project_pk)
    return render(request, 'projects/task_confirm_delete.html', {'task': task})

@login_required
def add_comment_to_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()
    return render(request, 'projects/add_comment_to_task.html', {'form': form, 'task': task})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'projects/task_detail.html', {'task': task})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})