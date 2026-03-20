from django.test import TestCase
from django.urls import reverse

from .views import  module_create
from . import services
from .models import Module, CustomUser

# class ModuleCreateViewTest(TestCase):
#     pass
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             username="testuser",
#             password="pass",
#             study_institution="VILNIUS TECH",
#             degree=CustomUser.DEGREE_BACHELOR,
#             name_of_program="Software Engineering",
#             start_year=2024,
#         )
#     def test_module_create_view(self):
#         self.client.login(username="testuser", password="pass")

#         response = self.client.post(reverse("module_create"), {
#             "title": "Biology",
#             "teacher": "Dr X",
#             "description": "Test"
#         })

#         self.assertEqual(response.status_code, 302)  
#         self.assertEqual(Module.objects.count(), 1)
        