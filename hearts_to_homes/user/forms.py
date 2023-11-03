from django.forms import ModelForm
from .models import UserProfile, ChildrensHome, Visit, Donation, Review


class AddHomesForm(ModelForm):
    class Meta:
        model = ChildrensHome
        fields = '__all__'


class AddProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

class EditHomesForm(ModelForm):
    class Meta:
        model = ChildrensHome
        fields = '__all__'

