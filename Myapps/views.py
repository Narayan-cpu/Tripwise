
from django.http import HttpResponse, request
from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def About(request):
    return render(request,'About.html')


import requests
from django.shortcuts import render

def travel_advisory(request):
    advisory_info = None
    error_message = None
    
    if request.method == "POST":
        country = request.POST.get('country', '').strip()
        if country:
            url = f"https://restcountries.com/v3.1/name/{country}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()[0]  # Fetch the first country match
                    advisory_info = {
                        "name": data.get("name", {}).get("common", "Unknown"),
                        "region": data.get("region", "Unknown"),
                        "subregion": data.get("subregion", "Unknown"),
                        "population": data.get("population", "Unknown"),
                        "advice": generate_advice(data.get("region", "Unknown"))  # Custom advice
                    }
                else:
                    error_message = "Country not found. Please check the spelling or try a different country."
            except requests.exceptions.RequestException as e:
                error_message = "Error fetching data. Please try again later."
    
    return render(request, "Advisory.html", {
        "advisory_info": advisory_info,
        "error_message": error_message
    })

def generate_advice(region):
    # Custom travel advice based on region
    advice_map = {
        "Africa": "Be cautious about health risks like malaria and ensure vaccinations are up-to-date.",
        "Asia": "Pay attention to local weather conditions and political situations.",
        "Europe": "Generally safe, but watch out for pickpocketing in crowded areas.",
        "Americas": "Some areas may have higher crime rates; research specific destinations.",
        "Oceania": "Ensure you have adequate travel insurance for remote locations."
    }
    return advice_map.get(region, "Exercise general travel precautions.")



# views.py
from django.shortcuts import render
from .models import Hotel

def hotel(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel.html', {'hotels': hotels})
from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.conf import settings
from decimal import Decimal
from .models import Hotel  # Assuming you have a Hotel model

def initiate_payment(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Ensure price is converted to a JSON serializable type
    amount = float(hotel.price_per_night)  # Convert Decimal to float

    # Generate a unique order ID
    order_id = f"BOOKING_{hotel_id}_123"  # Replace with your logic for user ID or use request.user.id

    # Dummy user data (you can replace this with actual user data when integrated)
    customer_name = "Hari Kumar"
    customer_email = "hari.kumar@example.com"
    customer_phone = "9999999993"

    # Cashfree Payment Gateway setup
    data = {
        "orderId": order_id,
        "orderAmount": amount,
        "orderCurrency": "INR",
        "customerName": customer_name,  # Dummy user's full name
        "customerEmail": customer_email,  # Dummy user's email
        "customerPhone": customer_phone,  # Dummy user's phone number
        "returnUrl": "http://127.0.0.1:8000/payment-success/",  # Update with your success endpoint
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.CASHFREE_SECRET_KEY}",
    }

    # Send POST request to Cashfree endpoint
    response = requests.post(
        f"{settings.CASHFREE_ENDPOINT}pg/orders", json=data, headers=headers
    )

    if response.status_code == 200:
        # Get the payment URL from the response
        payment_url = response.json().get("paymentLink")
        if payment_url:
            return redirect(payment_url)
        else:
            return render(request, 'payment_failed.html', {"error": "No payment link returned from the server."})
    else:
        # Render an error template if payment initiation fails
        return render(request, 'payment_failed.html', {"error": response.json()})


def payment_success(request):
    return render(request,'payment_successfull.html')


from django.shortcuts import render, redirect
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Display all posts
def community(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'community.html', {'posts': posts})

# Create a new post

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('community')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Add a comment

def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('community')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})

# Like a post

def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('community')
