from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .forms import JobApplicationForm, JobForm

# User Views
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

# Admin Views
@login_required
def admin_job_list(request):
    jobs = Job.objects.all()
    return render(request, 'admin_job_list.html', {'jobs': jobs})

@login_required
def admin_view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'admin_view_applications.html', {'applications': applications, 'job': job})

@login_required
def admin_add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')
    else:
        form = JobForm()
    return render(request, 'admin_add_job.html', {'form': form, 'action': 'Add'})

@login_required
def admin_edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'admin_edit_job.html', {'form': form, 'action': 'Edit'})

@login_required
def admin_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('admin_job_list')
