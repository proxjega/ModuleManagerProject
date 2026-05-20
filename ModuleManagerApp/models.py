from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    DEGREE_BACHELOR = "bachelor"
    DEGREE_MASTER = "master"
    DEGREE_DOCTORAL = "doctoral"
    
    DEGREE_CHOICES = [
    (DEGREE_BACHELOR, "Bachelor"),
    (DEGREE_MASTER, "Master"),
    (DEGREE_DOCTORAL, "Doctoral"),
    ]
    
    study_institution = models.CharField(max_length=50)
    degree = models.CharField(max_length=8, choices=DEGREE_CHOICES, default=DEGREE_BACHELOR)
    name_of_program = models.CharField(max_length=50)
    start_year = models.IntegerField(validators=[
        MinValueValidator(1970),
        MaxValueValidator(timezone.now().year + 1),
    ])
    
    def __str__(self):
        return self.username

class Module(models.Model):
    TYPE_OPTIONAL = "optional"
    TYPE_COMPULSORY = "compulsory"

    DELIVERY_F2F = "face-to-face"
    DELIVERY_REMOTE = "remote"
    
    LANGUAGE_LT = "lithuanian"
    LANGUAGE_EN = "english"

    TYPE_CHOICES = [
        (TYPE_COMPULSORY, "Compulsory"),
        (TYPE_OPTIONAL, "Optional")
    ]

    DELIVERY_CHOICES = [
        (DELIVERY_F2F, "Face-to-face"),
        (DELIVERY_REMOTE, "Remote")
    ]

    LANGUAGE_CHOICES=[
        (LANGUAGE_LT, "Lithuanian"),
        (LANGUAGE_EN, "English")
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    teacher = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    faculty = models.TextField(blank=True)
    module_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_COMPULSORY)
    delivery_mode = models.CharField(max_length=12, choices=DELIVERY_CHOICES, default=DELIVERY_F2F)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default=LANGUAGE_LT)
    credits =  models.IntegerField(default=5,
                                   validators=[
        MinValueValidator(1),
        MaxValueValidator(15),
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title