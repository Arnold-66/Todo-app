from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from .models import Task

def send_task_due_notifications():
    # Get current time and find tasks due within the next 24 hours
    current_time = now()
    upcoming_tasks = Task.objects.filter(
        due_date__gte=current_time, 
        due_date__lte=current_time + timedelta(days=1), 
        notification_sent=False
    )
    
    # Send email notifications for tasks due soon
    for task in upcoming_tasks:
        send_mail(
            'Task Due Soon',
            f"Your task '{task.title}' is due soon.",
            settings.DEFAULT_FROM_EMAIL,
            [task.user.email],  # Assuming Task model has a user field
            fail_silently=False,
        )
        
        task.notification_sent = True
        task.save()

class TaskDueNotificationCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)  # Run every hour
    code = 'todo_app.task_due_notification_cron_job'  # Unique identifier

    def do(self):
        send_task_due_notifications()  # Call the function to send notifications
