from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    
    # Admin URLs
    path('jobs/', views.admin_job_list, name='admin_job_list'),
    path('add/', views.admin_add_job, name='admin_add_job'),
    path('<int:job_id>/edit/', views.admin_edit_job, name='admin_edit_job'),
    path('delete/', views.admin_delete_job, name='admin_delete_job'),
    path('<int:job_id>/applications/', views.admin_view_applications, name='admin_view_applications'),
]
