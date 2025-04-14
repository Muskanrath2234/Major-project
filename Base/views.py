from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
import io
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import ContactForm
from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'services.html')

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                try:
                    send_mail(
                        'New Subscription',
                        f'A new subscription request has been received from {email}.',
                        'akankshamarathe19@gmail.com',
                        ['akankshamarathe19@gmail.com'],
                        fail_silently=False,
                    )

                    pdf_buffer = generate_pdf(email)

                    email_subject = "Subscription Confirmation"
                    email_body = f"Dear {email},\n\nThank you for subscribing to our service. Please find attached a confirmation PDF with your subscription details.\n\nBest regards,\nYour Company Name"
                    email_message = EmailMessage(
                        email_subject,
                        email_body,
                        'akankshamarathe19@gmail.com',
                        [email],
                    )
                    email_message.attach('subscription_details.pdf', pdf_buffer.read(), 'application/pdf')
                    email_message.send()

                    return JsonResponse({'status': 'success', 'message': 'Subscription successful. Check your email for confirmation.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
            else:
                return JsonResponse({'status': 'error', 'message': 'You have already subscribed.'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Email not provided.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def generate_pdf(email):
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer)
    p.drawString(100, 750, f"Subscription Confirmation")
    p.drawString(100, 730, f"Thank you for subscribing to our service.")
    p.drawString(100, 710, f"Email: {email}")
    p.showPage()
    p.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def base_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'admin' and user.is_superuser:
                auth_login(request, user)
                messages.info(request, f'{username}, You are logged in as Admin.')
                return redirect('home')
            elif role == 'user' and not user.is_superuser:
                auth_login(request, user)
                messages.info(request, f'{username}, You are logged in as User.')
                return redirect('User_post_list')
            else:
                messages.error(request, 'Invalid login credentials for the selected role.')
                return redirect('base_login')
        else:
            messages.error(request, 'Wrong username or password.')
            return redirect('base_login')

    return render(request, 'base_login.html')

from django.db import transaction

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def debug_print(msg, data):
    print(f"🔹 {msg}: {data}")

def recommend_companies(user_location, user_job_role, user_skills, top_n=5):
    try:
        import os
        from django.conf import settings

        # ✅ Load CSV File with Absolute Path
        csv_path = os.path.join(settings.BASE_DIR, "Base/static/ml_models/naukri_data_science_jobs_india.csv")
        df = pd.read_csv(csv_path)

        debug_print("CSV Loaded", df.head())

        # ✅ Normalize Column Names
        required_columns = ["Job_Role", "Company", "Location", "Skills/Description"]
        df.rename(columns={"Skills/Description": "Required_Skills"}, inplace=True)

        # ✅ Normalize Location for Filtering
        user_location = user_location.strip().lower()
        df["Location"] = df["Location"].str.lower().str.strip()

        filtered_jobs = df[df["Location"].str.contains(user_location, na=False)]
        debug_print("Filtered Jobs by Location", filtered_jobs.shape)

        if filtered_jobs.empty:
            debug_print("No jobs found", "Try another location")
            return []

        # ✅ Combine Job Role & Skills for Similarity
        filtered_jobs["combined_features"] = filtered_jobs["Job_Role"] + " " + filtered_jobs["Required_Skills"]
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

        debug_print("Recommended Jobs", recommended_jobs[["Company", "Job_Role", "Location"]])

        return recommended_jobs[["Company", "Job_Role", "Location", "Required_Skills", "Similarity Score"]].to_dict(orient="records")

    except Exception as e:
        debug_print("Exception Occurred", str(e))
        return []

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
