from django.test import TestCase
from django.urls import reverse

from . import forms

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
        
