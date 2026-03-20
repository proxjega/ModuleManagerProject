from django.test import TestCase

from .models import CustomUser
from . import services
from .models import Module

class CreateModuleServiceTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="pass",
            study_institution="VILNIUS TECH",
            degree=CustomUser.DEGREE_BACHELOR,
            name_of_program="Software Engineering",
            start_year=2024,
        )
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


class RegisterUserServiceTest(TestCase):
    def test_register_user_persists_and_can_be_read_back(self):
        data = {
            "username": "readeruser",
            "password1": "StrongPass123!",
            "first_name": "Reader",
            "last_name": "User",
            "email": "reader@example.com",
            "study_institution": "VGTU",
            "degree": CustomUser.DEGREE_DOCTORAL,
            "name_of_program": "Informatics",
            "start_year": 2023,
        }

        created_user = services.register_user(data)

        self.assertTrue(CustomUser.objects.filter(username="readeruser").exists())

        db_user = CustomUser.objects.get(username="readeruser")

        self.assertEqual(db_user.pk, created_user.pk)
        self.assertEqual(db_user.username, created_user.username)
        self.assertEqual(db_user.first_name, created_user.first_name)
        self.assertEqual(db_user.last_name, created_user.last_name)
        self.assertEqual(db_user.email, created_user.email)
        self.assertEqual(db_user.study_institution, created_user.study_institution)
        self.assertEqual(db_user.degree, created_user.degree)
        self.assertEqual(db_user.name_of_program, created_user.name_of_program)
        self.assertEqual(db_user.start_year, created_user.start_year)

    def test_register_user_creates_custom_user_with_expected_fields(self):
        data = {
            "username": "newuser",
            "password1": "StrongPass123!",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "study_institution": "Vilnius University",
            "degree": CustomUser.DEGREE_MASTER,
            "name_of_program": "Software Engineering",
            "start_year": 2025,
        }

        user = services.register_user(data)

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.study_institution, "Vilnius University")
        self.assertEqual(user.degree, CustomUser.DEGREE_MASTER)
        self.assertEqual(user.name_of_program, "Software Engineering")
        self.assertEqual(user.start_year, 2025)
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_register_user_uses_default_degree_when_not_provided(self):
        data = {
            "username": "nodegreeuser",
            "password1": "StrongPass123!",
            "first_name": "No",
            "last_name": "Degree",
            "email": "nodegree@example.com",
            "study_institution": "KTU",
            "name_of_program": "Computer Science",
            "start_year": 2024,
        }

        user = services.register_user(data)

        self.assertEqual(user.degree, CustomUser.DEGREE_BACHELOR)
        
