from django.core.management.base import BaseCommand, CommandError
import csv
import yaml
from codes.models import Artifact

class Command(BaseCommand):
    help="Load text artifacts from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('data_csv_file')
        parser.add_argument('column_yaml_file')

    def handle(self, *args, **options):
        with open(options['column_yaml_file']) as colfile:
            columns = yaml.load(colfile.read())

        with open(options['data_csv_file']) as infile:
            reader = csv.DictReader(infile)
            for student in reader:
                for column in columns:
                    artifact = Artifact(
                        text=student[column], 
                        user_id=student['id'],
                        column_id=column
                    )
                    artifact.save()
                        

