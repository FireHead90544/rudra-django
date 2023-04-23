from django.core.management.base import BaseCommand
from django.core.management import call_command
from os import system

class Command(BaseCommand):
    help = 'Builds the TailwindCSS file by invoking the npm script'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--runserver', action='store_true', help='Run the server after building the TailwindCSS file.')

    def handle(self, *args, **options):
        system('cd tailwind && npm run build && cd ..')
        if options['runserver']:
            call_command('runserver')