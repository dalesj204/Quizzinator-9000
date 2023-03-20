from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Runs makemigrations, migrate, runserver, createsuperuser, and test commands.'

    def handle(self, *args, **options):
        # Run makemigrations and migrate commands
        call_command('makemigrations','quizzes')
        call_command('migrate')

        # Run test command
        call_command('test')

        # Run the development server
        call_command('runserver')
