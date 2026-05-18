from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class SuccessfulRegistrationViewTest(TestCase):
	def test_successful_registration_redirects_when_accessed_directly(self):
		response = self.client.get(reverse("successful-registration"))

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("register"), fetch_redirect_response=False)

	def test_successful_registration_page_shows_login_button(self):
		session = self.client.session
		session["registration_successful"] = True
		session.save()

		response = self.client.get(reverse("successful-registration"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Registration successful")
		self.assertContains(response, "Go to login")
		self.assertContains(response, reverse("login"))


class RegisterViewTest(TestCase):
	def test_valid_registration_redirects_to_success_page(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "newstudent",
				"password1": "StrongPass123!",
				"password2": "StrongPass123!",
				"first_name": "New",
				"last_name": "Student",
				"email": "newstudent@example.com",
				"study_institution": "VILNIUS TECH",
				"degree": CustomUser.DEGREE_BACHELOR,
				"name_of_program": "Software Engineering",
				"start_year": 2024,
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("successful-registration"), fetch_redirect_response=False)
		self.assertTrue(CustomUser.objects.filter(username="newstudent").exists())
        