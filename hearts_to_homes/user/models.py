from django.db import models
# Create your models here.
class UserProfile(models.Model):
    full_name =models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} exists"

class ChildrensHome(models.Model):
    name = models.CharField(max_length=100)
    mission = models.TextField()
    vision = models.TextField()
    values = models.TextField()
    programs = models.TextField()
    needs = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='children_homes/',blank= True)
    def __str__(self):
        return f"{self.name}  is located at {self.location}"

class Donation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    childrens_home = models.ForeignKey(ChildrensHome, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}  has donated {self.amount}"



class Visit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    childrens_home = models.ForeignKey(ChildrensHome, on_delete=models.CASCADE)
    visit_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} has scheduled a visit for {self.visit_date}"

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    childrens_home = models.ForeignKey(ChildrensHome, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reviewed {self.childrens_home.name} with a rating of {self.rating}"


# class Admin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

#     def __str__(self):
#         return self.user.username

