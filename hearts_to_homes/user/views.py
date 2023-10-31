from django.shortcuts import render, redirect
from .models import Donation, ChildrensHome, UserProfile, Review, Visit
from .forms import ReviewForm, DonationForm, VisitForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')

def profile(request):
   profile = UserProfile.objects.all()
   return(request, 'register.html', {'profile':profile})

#Authentication
def loginpage(request):
  return render(request, 'login.html')
def registerpage(request):
  return render(request, 'register.html')

#Display reviews
def reviews(request):
  review = Review.objects.all()
  return render(request, 'register.html', {'review': review})

#Displays the events
def event(request):
  visit = Visit.objects.all()
  context = {
        "visit": visit,
    }
  return render(request, 'event.html',context)

#Display all homes
def children_homes(request):
  homes= ChildrensHome.objects.all()
  context = {
        "homes": homes,
    }
  return render(request, 'children_homes.html', context)

#Display list of donations
def donations(request):
  donations = Donation.objects.all()
  context = {
        'donations': donations,
    }
  return render(request, 'donations.html', context)
  
#Search for homes
def children_search(request):
    if 'query' in request.GET:
        query = request.GET['query']
    else:
        query = None

    if 'location' in request.GET:
        location = request.GET['location']
    else:
        location = None

    if query and location:
        results = ChildrensHome.objects.filter(name__icontains=query, location__icontains=location)
    elif query:
        results = ChildrensHome.objects.filter(name__icontains=query)
    elif location:
        results = ChildrensHome.objects.filter(location__icontains=location)
    else:
        results = None

    return render(request, 'children_homes_search.html', {'results': results})

#Info about a home
def children_detail(request, childrenshome_id):
    children_home = ChildrensHome.objects.get(id=childrenshome_id)
    return render(request, 'children_home_detail.html', {'children_home': children_home})

#Donations 
def make_donations(request, childrenshome_id):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.children_home = ChildrensHome.objects.get(id=childrenshome_id)
            donation.save()
    else:
        form = DonationForm()
    return render(request, 'donation_form.html', {'form': form})

#Visitation date
def schedule_visit(request, childrenshome_id):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.children_home = ChildrensHome.objects.get(id=childrenshome_id)
            visit.save()
    else:
        form = VisitForm()
    return render(request, 'visit_form.html', {'form': form})

#Create a review
def submit_review(request, childrenshome_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.children_home = ChildrensHome.objects.get(id=childrenshome_id)
            review.save()
    else:
        form = ReviewForm()

        return render(request, 'reviews/submit_review.html', {'form': form})