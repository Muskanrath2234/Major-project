from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    # Job-related fields
    Company= models.CharField(max_length=255, default="Unknown")  # 🔹 Company name
    published_on = models.DateField(auto_now_add=True)  # Auto-filled publish date
    Job_Role = models.CharField(max_length=100)  # Employment status (e.g., Full-time, Part-time)
    Job_Experience = models.CharField(max_length=100)  # Experience requirements (e.g., "2-5 years")
    Location = models.CharField(max_length=200)  # Location of the job
    Description = models.TextField(default="No description available")  

    def __str__(self):
        return self.title  # Display job title in admin panel or queries



class JobApplication(models.Model):
    # Foreign keys to link User and Job
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who is applying
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # Job being applied for

    # Additional application-related fields
    full_name = models.CharField(max_length=200)  # Applicant's full name
    email = models.EmailField()  # Applicant's email
    phone = models.CharField(max_length=15)  # Applicant's phone number
    resume = models.FileField(upload_to='resumes/')  # Resume file upload
    cover_letter = models.TextField(blank=True, null=True)  # Optional cover letter
    applied_on = models.DateTimeField(auto_now_add=True)  # Timestamp of application

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"  # Displays applicant name and job title
