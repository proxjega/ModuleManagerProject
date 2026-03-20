from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Module, CustomUser

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ["title", "teacher", "description"]
        
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "study_institution",
            "degree",
            "name_of_program",
            "start_year",
        )
        
class ProfileEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name",
            "last_name",
            "email",
            "study_institution",
            "degree",
            "name_of_program",
            "start_year",]