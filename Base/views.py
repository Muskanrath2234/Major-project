from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
import io
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import ContactForm

# Landing page view
def landing(request):
    return render(request, 'landing.html')

# About page view
def about(request):
    return render(request, 'about.html')

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Service page view
def service(request):
    return render(request, 'services.html')

# Subscribe view for handling email subscription
@csrf_exempt  # Disables CSRF protection for this view (be cautious with this)
def subscribe(request):
    if request.method == 'POST':  # Check if the request is a POST request
        email = request.POST.get('email')  # Get the email from the form submission
        if email:
            # Try to get or create a subscription for the given email
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                try:
                    # Send notification email to admin
                    send_mail(
                        'New Subscription',
                        f'A new subscription request has been received from {email}.',
                        'akankshamarathe19@gmail.com',  # Admin's email
                        ['akankshamarathe19@gmail.com'],  # List of recipients (admin)
                        fail_silently=False,  # Ensures failure raises an error
                    )

                    # Generate a PDF with subscription details
                    pdf_buffer = generate_pdf(email)

                    # Create an email message to send to the subscriber
                    email_subject = "Subscription Confirmation"
                    email_body = f"Dear {email},\n\nThank you for subscribing to our service. Please find attached a confirmation PDF with your subscription details.\n\nBest regards,\nYour Company Name"
                    email_message = EmailMessage(
                        email_subject,
                        email_body,
                        'akankshamarathe19@gmail.com',  # Sender's email
                        [email],  # Recipient's email (subscriber)
                    )
                    # Attach the generated PDF to the email
                    email_message.attach('subscription_details.pdf', pdf_buffer.read(), 'application/pdf')
                    email_message.send()  # Send the email

                    # Return a success response with a message
                    return JsonResponse(
                        {'status': 'success', 'message': 'Subscription successful. Check your email for confirmation.'})
                except Exception as e:
                    # Return an error response if email sending fails
                    return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
            else:
                # Return error if the email is already subscribed
                return JsonResponse({'status': 'error', 'message': 'You have already subscribed.'}, status=400)

        # Return error if no email was provided
        return JsonResponse({'status': 'error', 'message': 'Email not provided.'}, status=400)

    # Return error if the request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# Function to generate a PDF with subscription details
def generate_pdf(email):
    pdf_buffer = io.BytesIO()  # Create an in-memory buffer for the PDF
    p = canvas.Canvas(pdf_buffer)  # Create a canvas to draw the PDF
    p.drawString(100, 750, f"Subscription Confirmation")  # Add text to the PDF
    p.drawString(100, 730, f"Thank you for subscribing to our service.")
    p.drawString(100, 710, f"Email: {email}")
    p.showPage()  # End the current page
    p.save()  # Save the canvas (finalize the PDF)
    pdf_buffer.seek(0)  # Move buffer position to the start for reading
    return pdf_buffer  # Return the PDF buffer

# Login view for base user login (admin or regular user)
def base_login(request):
    if request.method == 'POST':  # Check if the request is a POST request
        username = request.POST.get('username')  # Get username from form
        password = request.POST.get('password')  # Get password from form
        role = request.POST.get('role')  # Get role (admin or user)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'admin' and user.is_superuser:  # If the role is admin and user is superuser
                auth_login(request, user)  # Log the admin user in
                messages.info(request, f'{username}, You are logged in as Admin.')  # Show success message
                return redirect('home')  # Redirect to the admin home page
            elif role == 'user' and not user.is_superuser:  # If the role is user and not a superuser
                auth_login(request, user)  # Log the regular user in
                messages.info(request, f'{username}, You are logged in as User.')  # Show success message
                return redirect('User_post_list')  # Redirect to user posts page
            else:
                messages.error(request, 'Invalid login credentials for the selected role.')  # Error for role mismatch
                return redirect('base_login')  # Redirect back to the login page
        else:
            messages.error(request, 'Wrong username or password.')  # Error for invalid credentials
            return redirect('base_login')  # Redirect back to the login page

    return render(request, 'base_login.html')  # Render the login page if GET request

# Contact form view to handle message submission
from django.db import transaction  # Import transaction management for atomic operations
def contact_view(request):
    if request.method == 'POST':  # Check if the request is a POST request
        form = ContactForm(request.POST)  # Get the form data from POST request
        if form.is_valid():  # Check if the form is valid
            with transaction.atomic():  # Ensure atomicity of database operations
                form.save()  # Save the form data to the database
            messages.success(request, 'Your message has been sent successfully!')  # Show success message
            return redirect('contact')  # Redirect to the contact page
        else:
            messages.error(request, 'Please correct the errors in the form.')  # Show error message for invalid form
    else:
        form = ContactForm()  # Initialize an empty form for GET request

    return render(request, 'contact.html', {'form': form})  # Render the contact page with the form


from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Debugging Function
def debug_print(msg, data):
    print(f"🔹 {msg}: {data}")

# ✅ Job Recommendation Function
def recommend_companies(user_location, user_job_role, user_skills, top_n=5):
    try:
        df = pd.read_csv("Base/static/ml_models/naukri_data_science_jobs_india.csv")

        # ✅ Check if data loaded properly
        debug_print("CSV Loaded", df.head())

        # ✅ Column Renaming (Ensure Consistency)
        df.rename(columns={"Company": "Company Name", "Skills/Description": "Required Skills"}, inplace=True)

        # ✅ Ensure Required Columns Exist
        required_columns = ["Company Name", "Job_Role", "Required Skills", "Location"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            debug_print("Error", f"Missing Columns: {missing_columns}")
            return []

        # ✅ Filter by Location
        filtered_jobs = df[df["Location"].str.contains(user_location, case=False, na=False)].copy()
        debug_print("Filtered Jobs by Location", filtered_jobs.shape)

        if filtered_jobs.empty:
            return []  # No jobs found, return empty list

        # ✅ Combine Job Role & Skills for Similarity
        filtered_jobs["combined_features"] = filtered_jobs["Job_Role"] + " " + filtered_jobs["Required Skills"]

        # ✅ User Profile Text
        user_profile = f"{user_job_role} {', '.join(user_skills)}"
        debug_print("User Profile", user_profile)

        # ✅ TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(filtered_jobs["combined_features"].tolist() + [user_profile])

        # ✅ Compute Similarity Scores
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # ✅ Add Similarity Scores & Sort
        filtered_jobs["Similarity Score"] = similarity_scores.flatten()
        recommended_jobs = filtered_jobs.sort_values(by="Similarity Score", ascending=False).head(top_n)

        debug_print("Recommended Jobs", recommended_jobs[["Company Name", "Job_Role", "Location"]])

        return recommended_jobs[["Company Name", "Job_Role", "Location", "Required Skills", "Similarity Score"]].to_dict(orient="records")

    except Exception as e:
        debug_print("Exception Occurred", str(e))
        return []

# ✅ Django View
def job_recommendations(request):
    jobs = []
    if request.method == "POST":
        user_location = request.POST.get("location", "").strip()
        user_job_role = request.POST.get("job_role", "").strip()
        user_skills = request.POST.get("skills", "").strip().split(",")

        if not user_location or not user_job_role or not user_skills:
            debug_print("Error", "Form fields missing!")
            return render(request, "recommendations.html", {"jobs": []})

        jobs = recommend_companies(user_location, user_job_role, user_skills)

    return render(request, "recommendations.html", {"jobs": jobs})
