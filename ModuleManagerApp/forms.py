from django.forms import ModelForm
from .models import Module

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ["title", "teacher", "description"]
        
