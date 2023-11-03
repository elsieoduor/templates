from django.shortcuts import render, redirect
from .models import Donation, ChildrensHome, UserProfile, Review, Visit
from .forms import ReviewForm, DonationForm, VisitForm, AddProfileForm, EditHomesForm

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from . import serializer
# from django.contrib.auth import authenticate

class UserView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response({'user': request.user.username})

class ChiefView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response({'chief': request.user.username})

class CreateAccountView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if not username or not password or not role:
            return Response({'error': 'Please provide all required fields'})

        user = UserProfile.objects.create_user(username=username, password=password, role=role)

        serializer = serializer.UserSerializer(user)

        return Response(serializer.data)

class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'})

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'})

        serializer = UserSerializer(user)

        return Response(serializer.data)

class ChildrenHomeListView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        children_homes = ChildrensHome.objects.all()
        return Response(children_homes.values())

class ChildrenHomeSearchView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        location = request.query_params.get('location')
        name = request.query_params.get('name')

        if location:
            children_homes = ChildrensHome.objects.filter(location=location)
        elif name:
            children_homes = ChildrensHome.objects.filter(name__icontains=name)
        else:
            children_homes = ChildrensHome.objects.all()

        return Response(children_homes.values())

class ChildrenHomeDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        children_home = ChildrensHome.objects.get(pk=pk)
        return Response(children_home.values())

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
            donation.children_home = ChildrensHome.objects.get(id=id)
            donation.save()
            return redirect('donations')
    else:
        form = DonationForm()
    return render(request, 'user/donation_form.html', {'form': form})

#Visitation date (requires authentication)
def schedule_visit(request, id):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.children_home = ChildrensHome.objects.get(id=id)
            visit.save()
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
    # user = UserProfile.objects.all()
    # homes = ChildrensHome.objects.all()
    # visits = Visit.objects.all().order_by("-date")[:5]  
    # context = {
    #     'user':user,
    #     'homes':homes,
    #     'visits':visits,
    # }
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
    pass

def add_home(request):
    pass
# def add(request):
#   if request.method == 'POST':
#     form = StudentForm(request.POST)
#     if form.is_valid():
#       new_student_number = form.cleaned_data['student_number']
#       new_first_name = form.cleaned_data['first_name']
#       new_last_name = form.cleaned_data['last_name']
#       new_email = form.cleaned_data['email']
#       new_field_of_study = form.cleaned_data['field_of_study']
#       new_gpa = form.cleaned_data['gpa']

#       new_student = Student(
#         student_number=new_student_number,
#         first_name=new_first_name,
#         last_name=new_last_name,
#         email=new_email,
#         field_of_study=new_field_of_study,
#         gpa=new_gpa
#       )
#       new_student.save()
#       return render(request, 'students/add.html', {
#         'form': StudentForm(),
#         'success': True
#       })
#   else:
#     form = StudentForm()
#   return render(request, 'students/add.html', {
#     'form': StudentForm()
#   })

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
    most_visited_home = ChildrensHome.objects.order_by('-visit').first()
    context = {'most_visited_home': most_visited_home}
    return render(request, 'chief/most_visited_home.html', context)

def most_in_need_home(request):
    most_in_need_home = ChildrensHome.objects.order_by('-needs').first()
    context = {'most_in_need_home': most_in_need_home}
    return render(request, 'chief/most_in_need_home.html', context)

