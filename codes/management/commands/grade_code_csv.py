from django.core.management.base import BaseCommand, CommandError
import csv
import yaml
from codes.models import Artifact, Code
from collections import defaultdict

class Command(BaseCommand):
    help="""
        Generate a csv file containing [0,1] for each grade and code.
    """

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('column_yaml_file')

    def handle(self, *args, **options):
        with open(options['column_yaml_file']) as colfile:
            columns = yaml.load(colfile.read())
        gradeCodes = [g + '_' + c.name for c in Code.objects.all() for g in ['6', '7', '8']]
        userdicts = {}
        for user_id in Artifact.user_ids():
            userdicts[user_id] = defaultdict(int)
            userdicts[user_id]['user_id'] = user_id
        for code in Code.objects.all():
            for artifact in code.artifacts.all():
                grade = artifact.column_id[0]
                if userdicts[artifact.user_id][grade + '_' + code.name] == 0:
                    userdicts[artifact.user_id][grade + '_' + code.name] = 1
        with open(options['filename'], 'w') as outfile:
            writer = csv.DictWriter(outfile, ['user_id'] + gradeCodes)
            writer.writeheader()
            writer.writerows(userdicts.values())
