from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Runs makemigrations, migrate, runserver, createsuperuser, and test commands.'

    def handle(self, *args, **options):

        # Run makemigrations and migrate commands
        call_command('makemigrations', 'quizzes')
        call_command('migrate')

        # Check if a superuser exists and create one if it doesn't
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            call_command('createsuperuser')

        # Run test command
        call_command('test')

        # Run the development server
        call_command('runserver')