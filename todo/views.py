from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.timezone import now


# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

@login_required
def tasklist(request):
    tasks = Task.objects.filter(user=request.user)

    # Handle checkbox toggle for completion status
    if request.method == 'POST' and 'task_id' in request.POST:
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        
        if 'completed' in request.POST:
            task.completed = True
        else:
            task.completed = False
        task.save()

        # Check if the request is AJAX by looking for the 'X-Requested-With' header
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'completed': task.completed})

    # Filter by completion status (Ongoing, Done, or All)
    status_filter = request.GET.get('status', None)
    if status_filter == 'done':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'ongoing':
        tasks = tasks.filter(completed=False)

    # Filter by due date (only tasks with due dates)
    due_filter = request.GET.get('due_date', None)
    if due_filter == 'due':
        tasks = tasks.filter(due_date__isnull=False)
    elif due_filter == 'no_due':
        tasks = tasks.filter(due_date__isnull=True)

    # Add task form handling
    if request.method == 'POST' and 'task_id' not in request.POST:
        taskform = TaskForm(request.POST)
        if taskform.is_valid():
            task = taskform.save(commit=False)
            task.user = request.user  # Set the user to the current logged-in user
            task.save()

            # Return the new task details including task id in the response for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'task': {
                        'id': task.id,
                        'title': task.title,
                        'completed': task.completed
                    }
                })

            messages.success(request, 'Task added successfully!')
            return redirect('tasklist')
    else:
        taskform = TaskForm()

    # Check if any task is due and send a message
    # Check if any task is due and send a message only if not completed
    for task in tasks:
        if not task.completed:  # Check if the task is not marked as completed
            if task.due_date and task.due_date <= now():  # Task is overdue or due today
                send_due_task_notification(request.user, task)


    tasks = tasks.order_by('-created_at')

    return render(request, 'todo/tasklist.html', {
        'tasks': tasks, 
        'taskform': taskform, 
        'status_filter': status_filter, 
        'due_filter': due_filter
    })

@login_required
def updatetask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure the task belongs to the logged-in user

    if request.method == 'POST':
        taskform = TaskForm(request.POST, instance=task)
        if taskform.is_valid():
            taskform.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasklist')
    else:
        taskform = TaskForm(instance=task)

    return render(request, 'todo/updatetask.html', {'taskform': taskform, 'task': task})


def send_due_task_notification(user, task):
    """Function to send notification when a task is due."""
    # Send email notification to the user (can be customized further)
    subject = f"Task Due: {task.title}"
    message = f"Dear {user.username},\n\nYour task '{task.title}' is due! Please take action.\n\nRegards,\nTask Manager"
    from_email = 'your_email@example.com'  # Replace with your email
    recipient_list = [user.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)


def deletetask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'task_id': task_id})
    
    messages.success(request, 'Task Deleted successfully!')
    return redirect('tasklist')



