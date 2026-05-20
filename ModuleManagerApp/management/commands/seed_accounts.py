from django.core.management.base import BaseCommand
from ModuleManagerApp.models import CustomUser, Module

class Command(BaseCommand):
    help = 'Seed database with test users and modules'

    def handle(self, *args, **options):
        # Create test admin
        if not CustomUser.objects.filter(username='admin').exists():
            user = CustomUser.objects.create_superuser(
                username='admin',
                password='admin',
                first_name='Admin',
                last_name='Admin',
                email='admin@example.com',
                study_institution='Vilnius University',
                degree=CustomUser.DEGREE_BACHELOR,
                name_of_program='Software Engineering',
                start_year=2024
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        # Create test user
        if not CustomUser.objects.filter(username='user').exists():
            user = CustomUser.objects.create_user(
                username='user',
                password='user1234',
                first_name='Test',
                last_name='User',
                email='test@example.com',
                study_institution='Vilnius University',
                degree=CustomUser.DEGREE_BACHELOR,
                name_of_program='Software Engineering',
                start_year=2024
            )
            self.stdout.write(self.style.SUCCESS('✓ Test user created'))

            # Create sample modules
            Module.objects.create(
                user=user,
                title='Programavimas Python',
                teacher='Tomas Plankis',
                description='Introduction to Python programming',
                faculty='Mathematics and Informatics faculty',
                module_type=Module.TYPE_COMPULSORY,
                delivery_mode=Module.DELIVERY_F2F,
                language=Module.LANGUAGE_LT,
                credits=5
            )
            self.stdout.write(self.style.SUCCESS('✓ Sample modules created'))
        else:
            self.stdout.write(self.style.WARNING('Test user already exists'))