from django.contrib import admin

# Register your models here.
from .models import ChildrensHome, Donation, Visit, Review, UserProfile

admin.site.register(ChildrensHome)
admin.site.register(Donation)
admin.site.register(Visit)
admin.site.register(Review)