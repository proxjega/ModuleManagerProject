from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Profile(models.Model):
    DEGREE_BACHELOR = "bachelor"
    DEGREE_MASTER = "master"
    DEGREE_DOCTORAL = "doctoral"
    
    DEGREE_CHOICES = [
    (DEGREE_BACHELOR, "Bachelor"),
    (DEGREE_MASTER, "Master"),
    (DEGREE_DOCTORAL, "Doctoral"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study_institution = models.CharField(max_length=50)
    degree = models.CharField(max_length=8, choices=DEGREE_CHOICES, default=DEGREE_BACHELOR)
    name_of_program = models.CharField(max_length=50)
    start_year = models.IntegerField(validators=[
        MinValueValidator(1970),
        MaxValueValidator(timezone.now().year + 1),
    ])
    

class Module(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    teacher = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title