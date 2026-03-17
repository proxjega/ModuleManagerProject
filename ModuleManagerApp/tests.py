from django.test import TestCase
from django.contrib.auth.models import User

from . import forms
from . import views
from . import services
from .models import Module

class ModuleFormTest(TestCase):
    def test_valid_form(self):
        form = forms.ModuleForm(data={
            "title":"Programavimas Python",
            "teacher":"Tomas Plankis",
            "description":"Desc"
        })
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        form = forms.ModuleForm(data={
            "title":"",
            "teacher":"Tomas Plankis",
            "description":"Desc"
        })
        self.assertFalse(form.is_valid())
        
class ModelCreateViewTest(TestCase):
    pass

class CreateModuleServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", password="pass")
    def test_create_module(self):
        data={
            "title":"Programavimas Python",
            "teacher":"Tomas Plankis",
            "description":"Desc"
        }
        module = services.create_module(self.user, data)
        self.assertEqual(module.title, "Programavimas Python")
        self.assertEqual(module.user, self.user)
        self.assertEqual(module.teacher, "Tomas Plankis")
        self.assertEqual(Module.objects.count(), 1)
        
