from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, SearchForm
from django.contrib.auth.decorators import login_required
from .models import User_Post
from django.db.models import Q

# Docstring at the top summarizing the file's purpose
"""
This views.py file contains views for handling user posts. 
It includes functionalities for creating, reading (listing), updating, and deleting posts.
Each view ensures appropriate access control based on user authentication.
"""

# Create a new post
@login_required
def create_post(request):
    """
    Handles the creation of a new post by a logged-in user.

    - If the request method is POST, it processes the form data to create a new post.
    - If the request method is GET, it displays an empty form for creating a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Creating form instance with submitted data
        if form.is_valid():  # Checking if the form data is valid
            post = form.save(commit=False)  # Saving the form instance without committing to the database
            post.user = request.user  # Assigning the logged-in user as the owner of the post
            post.save()  # Saving the post with the user data
            return redirect('User_post_list')  # Redirecting to the post list page after successful creation
    else:
        form = PostForm()  # Creating an empty form for GET request
    return render(request, 'User_create_post.html', {'form': form})  # Rendering the create post template with the form

# Create a new post
@login_required
def admin_create_post(request):
    """
    Handles the creation of a new post by a logged-in user.

    - If the request method is POST, it processes the form data to create a new post.
    - If the request method is GET, it displays an empty form for creating a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Creating form instance with submitted data
        if form.is_valid():  # Checking if the form data is valid
            post = form.save(commit=False)  # Saving the form instance without committing to the database
            post.user = request.user  # Assigning the logged-in user as the owner of the post
            post.save()  # Saving the post with the user data
            return redirect('admin_post_list')  # Redirecting to the post list page after successful creation
    else:
        form = PostForm()  # Creating an empty form for GET request
    return render(request, 'admin_create_post.html', {'form': form})  # Rendering the create post template with the form





# List all posts with search functionality
def admin_post_list(request):
    """
    Displays a list of all posts. Provides a search form for filtering posts by title,
    username, and date range.

    - Fetches all posts and allows filtering based on query, start date, and end date.
    """
    form = SearchForm(request.GET or None)  # Creating or getting an instance of the SearchForm with GET data
    posts = User_Post.objects.all().order_by('-created_at')  # Retrieving all posts ordered by creation date

    if form.is_valid():  # Checking if the form data is valid
        query = form.cleaned_data.get('query')  # Getting the search query
        start_date = form.cleaned_data.get('start_date')  # Getting the start date
        end_date = form.cleaned_data.get('end_date')  # Getting the end date

        if query:  # Filtering posts based on search query
            posts = posts.filter(Q(title__icontains=query) | Q(user__username__icontains=query))
        if start_date:  # Filtering posts based on start date
            posts = posts.filter(created_at__gte=start_date)
        if end_date:  # Filtering posts based on end date
            posts = posts.filter(created_at__lte=end_date)

    return render(request, 'admin_post_list.html', {'posts': posts, 'form': form})  # Rendering the post list with filtered results

# List all posts with search functionality
def post_list(request):
    """
    Displays a list of all posts. Provides a search form for filtering posts by title,
    username, and date range.

    - Fetches all posts and allows filtering based on query, start date, and end date.
    """
    form = SearchForm(request.GET or None)  # Creating or getting an instance of the SearchForm with GET data
    posts = User_Post.objects.all().order_by('-created_at')  # Retrieving all posts ordered by creation date

    if form.is_valid():  # Checking if the form data is valid
        query = form.cleaned_data.get('query')  # Getting the search query
        start_date = form.cleaned_data.get('start_date')  # Getting the start date
        end_date = form.cleaned_data.get('end_date')  # Getting the end date

        if query:  # Filtering posts based on search query
            posts = posts.filter(Q(title__icontains=query) | Q(user__username__icontains=query))
        if start_date:  # Filtering posts based on start date
            posts = posts.filter(created_at__gte=start_date)
        if end_date:  # Filtering posts based on end date
            posts = posts.filter(created_at__lte=end_date)

    return render(request, 'user_post_list.html', {'posts': posts, 'form': form})  # Rendering the post list with filtered results



# Update an existing post
@login_required
def update_post(request, pk):
    """
    Handles the updating of an existing post by the logged-in user.

    - If the request method is POST, it updates the post based on the submitted form data.
    - If the request method is GET, it displays the existing post in a form for editing.
    """
    post = get_object_or_404(User_Post, pk=pk, user=request.user)  # Retrieving the post with a given primary key (pk) and ensuring it belongs to the logged-in user
    if request.method == 'POST':  # Handling POST request for updating the post
        form = PostForm(request.POST, request.FILES, instance=post)  # Creating form instance with existing post data
        if form.is_valid():  # Checking if the form data is valid
            form.save()  # Saving the updated post data
            return redirect('User_post_list')  # Redirecting to the post list page after successful update
    else:
        form = PostForm(instance=post)  # Creating form with existing post data for GET request
    return render(request, 'User_update_post.html', {'form': form, 'post': post})  # Rendering the update post template with the form and post data





# Update an existing post
@login_required
def admin_update_post(request, pk):
    """
    Handles the updating of an existing post by the logged-in user.

    - If the request method is POST, it updates the post based on the submitted form data.
    - If the request method is GET, it displays the existing post in a form for editing.
    """
    post = get_object_or_404(User_Post, pk=pk, user=request.user)  # Retrieving the post with a given primary key (pk) and ensuring it belongs to the logged-in user
    if request.method == 'POST':  # Handling POST request for updating the post
        form = PostForm(request.POST, request.FILES, instance=post)  # Creating form instance with existing post data
        if form.is_valid():  # Checking if the form data is valid
            form.save()  # Saving the updated post data
            return redirect('admin_post_list')  # Redirecting to the post list page after successful update
    else:
        form = PostForm(instance=post)  # Creating form with existing post data for GET request
    return render(request, 'admin_update_post.html', {'form': form, 'post': post})  # Rendering the update post template with the form and post data





# Delete a post
@login_required
def delete_post(request, pk):
    """
    Handles the deletion of a post by the logged-in user.

    - If the request method is POST, it deletes the specified post.
    - If the request method is GET, it prompts the user to confirm deletion.
    """
    post = get_object_or_404(User_Post, pk=pk, user=request.user)  # Retrieving the post with a given primary key (pk) and ensuring it belongs to the logged-in user
    if request.method == 'POST':  # Handling POST request for deleting the post
        post.delete()  # Deleting the post
        return redirect('User_post_list')  # Redirecting to the post list page after successful deletion
    return render(request, 'User_delete_post.html', {'post': post})  # Rendering the delete post template with the post data


# Delete a post
@login_required
def admin_delete_post(request, pk):
    """
    Handles the deletion of a post by the logged-in user.

    - If the request method is POST, it deletes the specified post.
    - If the request method is GET, it prompts the user to confirm deletion.
    """
    post = get_object_or_404(User_Post, pk=pk, user=request.user)  # Retrieving the post with a given primary key (pk) and ensuring it belongs to the logged-in user
    if request.method == 'POST':  # Handling POST request for deleting the post
        post.delete()  # Deleting the post
        return redirect('admin_post_list')  # Redirecting to the post list page after successful deletion
    return render(request, 'admin_delete_post.html', {'post': post})  # Rendering the delete post template with the post data