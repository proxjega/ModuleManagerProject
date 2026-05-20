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


class RedactModuleServiceTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="pass",
            study_institution="VILNIUS TECH",
            degree=CustomUser.DEGREE_BACHELOR,
            name_of_program="Software Engineering",
            start_year=2024,
        )
        self.module = Module.objects.create(
            user=self.user,
            title="Programavimas Python",
            teacher="Tomas Plankis",
            description="Original description"
        )

    def test_redact_module_updates_teacher(self):
        data = {
            "teacher": "New Teacher",
            "description": "Original description"
        }
        services.redact_module(self.module.id, data)
        
        updated_module = Module.objects.get(pk=self.module.id)
        self.assertEqual(updated_module.teacher, "New Teacher")
        self.assertEqual(updated_module.description, "Original description")

    def test_redact_module_updates_description(self):
        data = {
            "teacher": "Tomas Plankis",
            "description": "Updated description"
        }
        services.redact_module(self.module.id, data)
        
        updated_module = Module.objects.get(pk=self.module.id)
        self.assertEqual(updated_module.teacher, "Tomas Plankis")
        self.assertEqual(updated_module.description, "Updated description")

    def test_redact_module_updates_both_fields(self):
        data = {
            "teacher": "Another Teacher",
            "description": "Completely new description"
        }
        services.redact_module(self.module.id, data)
        
        updated_module = Module.objects.get(pk=self.module.id)
        self.assertEqual(updated_module.teacher, "Another Teacher")
        self.assertEqual(updated_module.description, "Completely new description")

    def test_redact_module_preserves_title_and_user(self):
        data = {
            "teacher": "New Teacher",
            "description": "New description"
        }
        services.redact_module(self.module.id, data)
        
        updated_module = Module.objects.get(pk=self.module.id)
        self.assertEqual(updated_module.title, "Programavimas Python")
        self.assertEqual(updated_module.user, self.user)

    def test_redact_module_handles_missing_fields(self):
        data = {
            "teacher": "Updated Teacher"
        }
        services.redact_module(self.module.id, data)
        
        updated_module = Module.objects.get(pk=self.module.id)
        self.assertEqual(updated_module.teacher, "Updated Teacher")
        self.assertEqual(updated_module.description, "Original description")


class DeleteModuleServiceTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="pass",
            study_institution="VILNIUS TECH",
            degree=CustomUser.DEGREE_BACHELOR,
            name_of_program="Software Engineering",
            start_year=2024,
        )
        self.module = Module.objects.create(
            user=self.user,
            title="Programavimas Python",
            teacher="Tomas Plankis",
            description="Test description"
        )

    def test_delete_module_removes_from_database(self):
        self.assertEqual(Module.objects.count(), 1)
        
        services.delete_module(self.module.id)
        
        self.assertEqual(Module.objects.count(), 0)

    def test_delete_module_specific_module_deleted(self):
        module2 = Module.objects.create(
            user=self.user,
            title="Another Module",
            teacher="Another Teacher",
            description="Another description"
        )
        
        services.delete_module(self.module.id)
        
        self.assertEqual(Module.objects.count(), 1)
        self.assertTrue(Module.objects.filter(pk=module2.id).exists())
        self.assertFalse(Module.objects.filter(pk=self.module.id).exists())

    def test_delete_module_does_not_affect_other_users_modules(self):
        other_user = CustomUser.objects.create_user(
            username="otheruser",
            password="pass",
            study_institution="KTU",
            degree=CustomUser.DEGREE_MASTER,
            name_of_program="Computer Science",
            start_year=2023,
        )
        other_module = Module.objects.create(
            user=other_user,
            title="Other Module",
            teacher="Other Teacher",
            description="Other description"
        )
        
        services.delete_module(self.module.id)
        
        self.assertEqual(Module.objects.count(), 1)
        self.assertTrue(Module.objects.filter(pk=other_module.id).exists())
        
