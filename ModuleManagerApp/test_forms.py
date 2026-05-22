from django.test import TestCase
from .forms import (
    ModuleForm,
    ModuleRedactForm,
    RegisterForm,
    ProfileEditForm,
    PdfForm,
)
from .models import Module, CustomUser


class ModuleFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            study_institution="Test University",
            degree="bachelor",
            name_of_program="Test Program",
            start_year=2020,
        )

    def test_module_form_valid(self):
        form_data = {
            "title": "Python Programming",
            "teacher": "Dr. Smith",
            "description": "Learn Python basics",
            "faculty": "Computer Science",
            "module_type": "compulsory",
            "delivery_mode": "face-to-face",
            "language": "english",
            "credits": 5,
        }
        form = ModuleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_module_form_invalid(self):
        form_data = {
            "title": "",  
            "teacher": "Dr. Smith",
            "credits": 20, 
        }
        form = ModuleForm(data=form_data)
        self.assertFalse(form.is_valid())


class ModuleRedactFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            study_institution="Test University",
            degree="bachelor",
            name_of_program="Test Program",
            start_year=2020,
        )
        self.module = Module.objects.create(
            user=self.user,
            title="Original Title",
            teacher="Dr. Original",
            description="Original description",
            faculty="Computer Science",
            module_type="compulsory",
            delivery_mode="face-to-face",
            language="english",
            credits=5,
        )

    def test_module_redact_form_valid(self):
        form_data = {
            "teacher": "Dr. NewTeacher",
            "description": "Updated description",
            "faculty": "Engineering",
            "module_type": "optional",
            "delivery_mode": "remote",
            "language": "lithuanian",
            "credits": 8,
        }
        form = ModuleRedactForm(data=form_data, instance=self.module)
        self.assertTrue(form.is_valid())

    def test_module_redact_form_invalid(self):
        form_data = {
            "teacher": "Dr. NewTeacher",
            "credits": 0,  
            "module_type": "invalid", 
        }
        form = ModuleRedactForm(data=form_data, instance=self.module)
        self.assertFalse(form.is_valid())


class RegisterFormTest(TestCase):
    def test_register_form_valid(self):
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "study_institution": "Test University",
            "degree": "bachelor",
            "name_of_program": "Computer Science",
            "start_year": 2020,
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "password1": "short",  
            "password2": "different", 
            "study_institution": "Test University",
            "degree": "invalid", 
            "name_of_program": "Computer Science",
            "start_year": 2020,
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            study_institution="Test University",
            degree="bachelor",
            name_of_program="Test Program",
            start_year=2020,
        )

    def test_profile_edit_form_valid(self):
        form_data = {
            "first_name": "Janet",
            "last_name": "Smithson",
            "email": "janet@example.com",
            "study_institution": "New University",
            "degree": "master",
            "name_of_program": "Advanced Program",
            "start_year": 2021,
        }
        form = ProfileEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_edit_form_invalid(self):
        form_data = {
            "first_name": "Janet",
            "email": "invalid-email",  
            "study_institution": "New University",
            "degree": "invalid",  
            "name_of_program": "Advanced Program",
            "start_year": 2026, 
        }
        form = ProfileEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())


class PdfFormTest(TestCase):
    def test_pdf_form_valid(self):
        form_data = {
            "filename": "my_modules_report.pdf",
        }
        form = PdfForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pdf_form_invalid(self):
        form_data = {
            "filename": "", 
        }
        form = PdfForm(data=form_data)
        self.assertFalse(form.is_valid())
