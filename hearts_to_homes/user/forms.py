from django.forms import ModelForm
from .models import UserProfile, ChildrensHome, Visit, Donation, Review


class AddHomesForm(ModelForm):
    class Meta:
        model = ChildrensHome
        fields = ["name", "vision", "mission", "needs", "location", "image", "values", "programs"]


class AddProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "username", "email", "password"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = ['visit_date']

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']

