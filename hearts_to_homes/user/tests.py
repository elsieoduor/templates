
from django.test import TestCase
from .models import UserProfile, ChildrensHome, Donation, Visit, Review
from django.urls import reverse
from .views import home
from django.contrib.auth.models import User
from .forms import AddProfileForm, AddHomesForm, ReviewForm, VisitForm, DonationForm, EditHomesForm, CustomUserCreationForm
from .serializer import UserSerializer, ChildrenHomeSerializer, DonationSerializer, VisitSerializer, ReviewSerializer
# Create your tests here.

class ModelTestCase(TestCase):
    def test_create_user_profile(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        self.assertEqual(user.username, "testuser")
    
    def test_create_children_home(self):
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        self.assertEqual(home.name, "Test Home")

    def test_create_donation(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        donation = Donation.objects.create(user=user, childrens_home=home, amount=100, donated_item='money')
        self.assertEqual(donation.amount, 100)

    def test_create_visit(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        visit = Visit.objects.create(user=user, childrens_home=home, visit_date='2023-12-31 12:00:00')
        self.assertEqual(visit.visit_date.strftime('%Y-%m-%d %H:%M:%S'), '2023-12-31 12:00:00')

    def test_create_review(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        review = Review.objects.create(user=user, childrens_home=home, rating=4, comment="Test comment")
        self.assertEqual(review.rating, 4)

#For views
class ViewTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'default/home.html')

    def test_children_homes_view(self):
        ChildrensHome.objects.create(name="Test Home", location="Test Location")
        response = self.client.get(reverse('children_homes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'default/children_homes.html')
        self.assertEqual(len(response.context['homes']), 1)
    
    def test_event_view(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_children_search_view(self):
        response = self.client.get('/children_homes/search/')
        self.assertEqual(response.status_code, 200)

    def test_children_detail_view(self):
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        response = self.client.get(reverse('children_home_detail', args=[home.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Home")
        self.assertContains(response, "Test Location")

    def test_make_donations_view(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        response = self.client.post(reverse('make_donations', args=[home.id]), {'user': user.id, 'childrens_home': home.id, 'amount': 100, 'donated_item': 'money'})
        self.assertEqual(response.status_code, 302)  
    def test_schedule_visit_view(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        response = self.client.post(reverse('schedule_visit', args=[home.id]), {'user': user.id, 'childrens_home': home.id, 'visit_date': '2023-12-31 12:00:00'})
        self.assertEqual(response.status_code, 302)  

    def test_submit_review_view(self):
        user = UserProfile.objects.create(username="testuser", email="test@example.com", password="testpassword")
        home = ChildrensHome.objects.create(name="Test Home", location="Test Location")
        response = self.client.post(reverse('submit_review', args=[home.id]), {'user': user.id, 'childrens_home': home.id, 'rating': 5, 'comment': 'Great home!'})
        self.assertEqual(response.status_code, 302)  

#For forms
class FormTestCase(TestCase):
    def test_add_homes_form_valid(self):
        data = {'name': 'Test Home', 'location': 'Test Location'}
        form = AddHomesForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_profile_form_valid(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = AddProfileForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_add_profile_form(self):
        form_data = {'full_name': 'Test User', 'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        form = AddProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_homes_form(self):
        form_data = {'name': 'Test Home', 'location': 'Test Location', 'needs_food': 10, 'needs_money': 5}
        form = AddHomesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form(self):
        form_data = {'rating': 5, 'comments': 'Great home!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_visit_form(self):
        form_data = {'visit_date': '2023-12-31 12:00:00'}
        form = VisitForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_donation_form(self):
        form_data = {'amount': 100, 'donated_item': 'money'}
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_homes_form(self):
        home_data = {'name': 'Test Home', 'location': 'Test Location', 'needs_food': 10, 'needs_money': 5}
        home = AddHomesForm(data=home_data)
        home.save()
        home_instance = ChildrensHome.objects.get(name='Test Home')
        form_data = {'name': 'Updated Home', 'location': 'Updated Location'}
        form = EditHomesForm(data=form_data, instance=home_instance)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form(self):
        form_data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

#For serializers
class SerializerTestCase(TestCase):
    def test_user_serializer(self):
        user = UserProfile.objects.create(username='testuser', email='test@example.com', name='Test User')
        serializer = UserSerializer(instance=user)
        self.assertEqual(serializer.data['username'], 'testuser')

    def test_children_home_serializer(self):
        home = ChildrensHome.objects.create(name='Test Home', location='Test Location', needs_food=10, needs_money=5)
        serializer = ChildrenHomeSerializer(instance=home)
        self.assertEqual(serializer.data['name'], 'Test Home')

    def test_donation_serializer(self):
        user = UserProfile.objects.create(username='testuser', email='test@example.com', name='Test User')
        home = ChildrensHome.objects.create(name='Test Home', location='Test Location')
        donation = Donation.objects.create(user=user, childrens_home=home, amount=100, donated_item='money')
        serializer = DonationSerializer(instance=donation)
        self.assertEqual(serializer.data['amount'], 100)

    def test_visit_serializer(self):
        user = UserProfile.objects.create(username='testuser', email='test@example.com', name='Test User')
        home = ChildrensHome.objects.create(name='Test Home', location='Test Location')
        visit = Visit.objects.create(user=user, childrens_home=home, visit_date='2023-12-31 12:00:00')
        serializer = VisitSerializer(instance=visit)
        self.assertEqual(serializer.data['user'], user.id)

    def test_review_serializer(self):
        user = UserProfile.objects.create(username='testuser', email='test@example.com', name='Test User')
        home = ChildrensHome.objects.create(name='Test Home', location='Test Location')
        review = Review.objects.create(user=user, childrens_home=home, rating=5, comment='Great home!')
        serializer = ReviewSerializer(instance=review)
        self.assertEqual(serializer.data['rating'], 5)