from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command, get_commands
from django.apps import apps
import traceback


class Seed(BaseCommand):
    help = "Run seeder from all installed Apps."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear tables before seeder.'
        )

        parser.add_argument(
            '--only',
            nargs='+',
            type=str,
            help='Run specific installed app seed. (e.g. python manage.py seed --only users products)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting seeders.'))

        all_commands = get_commands()
        seed_commands = []

        if options['only']:
            seed_commands = [cmd for cmd in seed_commands if cmd in options['only']]

        for cmd_name, app_name in all_commands.items():
            if cmd_name.endswith("_seed") and app_name != "__main__":
                if app_name in [a.name for a in apps.get_app_configs()]:
                    seed_commands.append(cmd_name)



        return seed_commands