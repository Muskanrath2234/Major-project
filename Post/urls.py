from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for creating a new post
    path('create/', views.create_post, name='User_create_post'),  
    # URL pattern for listing all posts
    path('', views.post_list, name='User_post_list'), 
     path('adminpost/', views.admin_post_list, name='admin_post_list'),  
    # URL pattern for updating an existing post identified by its primary key (pk)
    path('<int:pk>/update/', views.update_post, name='User_update_post'),  
    # URL pattern for deleting a post identified by its primary key (pk)
    path('<int:pk>/delete/', views.delete_post, name='User_delete_post'),  
]