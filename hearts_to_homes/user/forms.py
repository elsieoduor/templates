from django.forms import ModelForm
from .models import UserProfile, ChildrensHome, Visit, Donation, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

    def clean(self):
        cleaned_data = super().clean()
        donated_item = cleaned_data.get('donated_item')
        amount = cleaned_data.get('amount')

        if donated_item != 'money' and amount:
            self.add_error('amount', "Amount should only be specified for money donations.")

        return cleaned_data

class EditHomesForm(ModelForm):
    class Meta:
        model = ChildrensHome
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')