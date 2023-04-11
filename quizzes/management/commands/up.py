from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.test.runner import DiscoverRunner
import sys, os, subprocess
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Runs all tests and prints the result on the terminal'

    def handle(self, *args, **options):
        call_command('build')
        # Redirect stdout to a file
        sys.stdout = open('temp', 'w')

        # Run the tests using the DiscoverRunner
        test_runner = DiscoverRunner()
        test_runner.run_tests(['quizzes'])

        # Reset stdout to the console
        sys.stdout = sys.__stdout__

        # Read the contents of the file and count occurrences of the keywords
        with open('temp', 'r') as f:
            test_output = f.read()
            unittest_count = test_output.count('UnitTest')
            tested_count = test_output.count('Tested')
        
        # Get the current git username
        git_username = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()

        # Get the current time in the GMT-4 timezone and format it as "YYYY-MM-DD_HH-MM-SS"
        time_zone = pytz.timezone("US/Eastern")
        time_now = datetime.now(time_zone).strftime('%Y-%m-%d_%H-%M-%S')

        # Create the file path with the folder name and filename
        file_path = os.path.join('test_log', f'{git_username}_{time_now}.csv')

        # Write the counts to the file with the created file path
        with open(file_path, 'w') as f:
            f.write(f"Unittest: {unittest_count}\n")
            f.write(f"Passed: {tested_count}\n")

        # Run tests and clean up the temporary file
        call_command('test')
        os.remove('temp')