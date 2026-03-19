from django.test import TestCase

from .models import CustomUser
from . import services
from .models import Module

class CreateModuleServiceTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser", password="pass")
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
        
