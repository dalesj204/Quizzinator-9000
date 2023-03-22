from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Clean all files listed in .gitignore'

    def handle(self, *args, **options):
        with open('.gitignore', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    os.system(f'rm -rf {line}')
        self.stdout.write(self.style.SUCCESS('Successfully cleaned all files listed in .gitignore'))