from django.forms import ModelForm, Form, CharField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Module, CustomUser

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ["title", "teacher", "description", "faculty", "module_type", "delivery_mode", "language", "credits"]

class ModuleRedactForm(ModelForm):
    class Meta:
        model = Module
        fields = ["teacher", "description", "faculty", "module_type", "delivery_mode", "language", "credits"]
        
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
        
class PdfForm(Form):
    filename = CharField(
        max_length=200,
        label="Choose the name for generated pdf file"
    )