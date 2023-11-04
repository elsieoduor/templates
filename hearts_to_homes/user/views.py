from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import F
from .models import Donation, ChildrensHome, UserProfile, Review, Visit
from .forms import ReviewForm, DonationForm, VisitForm, AddProfileForm, EditHomesForm, AddHomesForm, UserCreationForm


# Create your views here.
def home(request):
  return render(request, 'default/home.html')

def dashboard(request):
  return render(request, 'user/dashboard.html')

def about(request):
  return render(request, 'default/about.html')

def contact(request):
  return render(request, 'default/contact.html')

def profile(request):
   profile = UserProfile.objects.all()
   return(request, 'chief/user.html', {'profile':profile})

#Authentication
def loginpage(request):
  if request.method == "POST":
     username = request.POST['username']
     password = request.POST['password']
     user = UserProfile.objects.filter(username=username, password=password).count()
     if user > 0:
        user=UserProfile.objects.filter(username=username,password=password).first()
        request.session['loginpage']=True
        request.session['userid']=user.id
        return redirect('/dashboard')
  else:
    form = AddProfileForm()
  return render(request, 'user/login.html', {'form':form})

def registerpage(request):
	if request.method=='POST':
		form=AddProfileForm(request.POST)
		if form.is_valid():
			form.save()
			
	form=AddProfileForm()
	return render(request, 'user/register.html',{'form':form,})

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
  return render(request, 'default/event.html',context)

#Display all homes (requires authentication)
def children_homes(request):
  homes= ChildrensHome.objects.all()
  context = {
        "homes": homes,
    }
  return render(request, 'default/children_homes.html', context)

#Display list of donations
def donations(request):
  donations = Donation.objects.all()
  context = {
        'donations': donations,
    }
  return render(request, 'default/donations.html', context)
  
#Search for homes (requires authentication)
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

    return render(request, 'default/children_homes_search.html', {'results': results})

#Info about a home (requires authentication)
def children_detail(request, id):
    children_home = ChildrensHome.objects.get(id=id)
    return render(request, 'default/children_home_detail.html', {'children_home': children_home})

#Donations (requires authentication)
def make_donations(request,id):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            children_home = ChildrensHome.objects.get(id=id)

            # Update needs based on the type of donation made
            if donation.donated_item == 'clothes':
                ChildrensHome.objects.filter(id=id).update(needs_clothes=F('needs_clothes') - 1)
            elif donation.donated_item == 'hygiene':
                ChildrensHome.objects.filter(id=id).update(needs_hygiene_supplies=F('needs_hygiene_supplies') - 1)
            elif donation.donated_item == 'food':
                ChildrensHome.objects.filter(id=id).update(needs_food=F('needs_food') - 1)
            elif donation.donated_item == 'money':
                ChildrensHome.objects.filter(id=id).update(needs_money=F('needs_money') - 1)

            donation.childrens_home = children_home
            donation.save()
            return redirect('donations')
    else:
        form = DonationForm()
    return render(request, 'user/donation_form.html', {'form': form})

#Visitation date (requires authentication)
def schedule_visit(request, id):
    user_visits = Visit.objects.filter(user=request.user, visit_date__gte=timezone.now())
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            home = ChildrensHome.objects.get(id=id)
            visit.childrens_home = home
            visit.save()

            # Increment the visit count for the home
            home.visit += 1
            home.save()

            return redirect('events')
    else:
        form = VisitForm()
    return render(request, 'user/visit_form.html', {'form': form})


#Create a review (requires authentication)
def submit_review(request,id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.children_home = ChildrensHome.objects.get(id=id)
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

        return render(request, 'user/submit_review.html', {'form': form})



#Chief part  
def chief_dashboard(request):  
    return render(request,'chief/dashboard.html')

def chief_loginpage(request):
    pass

def chief_registerpage(request):
    pass

def all_users(request):
    user = UserProfile.objects.all()
    context={'user':user}
    return render(request,'chief/all_users.html',context)

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users') 
    else:
        form = UserCreationForm()

    return render(request, 'chief/add_user.html', {'form': form})

def add_home(request):
  if request.method == 'POST':
        form = AddHomesForm(request.POST, request.FILES)
        if form.is_valid():
            new_home = form.save(commit=False)
            new_home.save()
            return redirect('children_homes', id=new_home.id)  
  else:
        form = AddHomesForm()
  return render(request, 'chief/add_home.html', {'form': form})

def edit_home(request, id):
    if request.method == 'POST':
        home = ChildrensHome.objects.get(id=id)
        form = EditHomesForm(request.POST, instance=home)
        if form.is_valid:
            form.save()
            return redirect('children_home_detail')
    else:
        home = ChildrensHome.objects.get(id=id)
        form = EditHomesForm(instance=home)
    return render(request, 'chief/homes.html', {'form':form})

def delete_home(request, id):
    home = ChildrensHome.objects.get(id=id)
    if request.method == 'POST':
        home.delete()
        return redirect('chief_dashboard') 

    context = {'home': home}
    return render(request, 'chief/delete_home.html', context)

#Analytics of the homes
def most_visited_home(request):
    upcoming_visits = Visit.objects.filter(visit_date__gte=timezone.now())
    most_visited_home = ChildrensHome.objects.order_by('-visit').first()
    context = {'most_visited_home': most_visited_home, "upcoming_visits": upcoming_visits}
    return render(request, 'chief/most_visited_home.html', context)

def most_in_need_home(request):
    most_in_need_home = ChildrensHome.objects.order_by('-needs').first()
    context = {'most_in_need_home': most_in_need_home}
    return render(request, 'chief/most_in_need_home.html', context)

