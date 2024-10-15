from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    gender = models.CharField(max_length=1)
    region = models.CharField(max_length=100)
    highest_education = models.CharField(max_length=100)
    imd_band = models.CharField(max_length=10)
    age_band = models.CharField(max_length=10)
    num_of_prev_attempts = models.IntegerField()
    is_banked = models.IntegerField()
    code_module_x = models.CharField(max_length=10)
    code_presentation_x = models.CharField(max_length=10)
    code_module_y = models.CharField(max_length=10)
    code_presentation_y = models.CharField(max_length=10)
    results = models.CharField(max_length=100)
    def __str__(self):
        return f"StudentResults {self.id}"  
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.username    