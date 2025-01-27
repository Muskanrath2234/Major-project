from django.db import models
from django.contrib.auth.models import User

# Ticket status choices
STATUS_CHOICES = [
    ('arrived', 'Arrived'),            # Ticket has arrived for processing
    ('working', 'Working'),            # Ticket is currently being worked on
    ('solved', 'Solved'),              # Ticket has been resolved
]

# Common issue choices
ISSUE_CHOICES = [
    ('Company Policies', 'Company Policies'),            # Issues related to company rules and policies
    ('Salary Delays', 'Salary Delays'),                  # Issues related to delayed salary payments
    ('Workload Pressure', 'Workload Pressure'),          # Issues related to excessive workload
    ('Workplace Harassment', 'Workplace Harassment'),    # Issues related to harassment or discrimination
    ('Software Bugs', 'Software Bugs'),                  # Issues in software or internal tools
    ('Technical Support', 'Technical Support'),          # Issues with tech support or IT department
    ('Job Role Mismatch', 'Job Role Mismatch'),          # Job role not matching the job description
    ('Project Deadlines', 'Project Deadlines'),          # Problems meeting deadlines or unrealistic expectations
    ('Performance Reviews', 'Performance Reviews'),      # Issues related to biased performance reviews
    ('Team Collaboration', 'Team Collaboration')         # Issues with team dynamics or cooperation
]


"""
This file contains the models for managing support tickets within the application.
It defines the Ticket model with fields for user association, issue type, custom issues, status, and timestamps.
"""

# Ticket Model
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ticket raised by a user
    issue_type = models.CharField(max_length=50, choices=ISSUE_CHOICES)  # Type of issue
    custom_issue = models.CharField(max_length=255, blank=True, null=True)  # Field for custom issues, optional
    description = models.TextField()  # Detailed description of the issue
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='arrived')  # Current status of the ticket
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the ticket is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the ticket is last updated

    def __str__(self):
        return f'{self.user.username} - {self.get_issue_type_display()} - {self.status}'

