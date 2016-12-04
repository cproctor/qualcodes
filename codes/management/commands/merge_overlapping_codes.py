from django.core.management.base import BaseCommand, CommandError
import yaml
from codes.models import Artifact, Code

class Command(BaseCommand):
    help="""
        Given a YAML file specifying [{newCode: [oldCode,...], ... }, ...], 
        creates new codes, adds artifacts in each oldCode, and deletes oldCodes.
    """

    def add_arguments(self, parser):
        parser.add_argument('merge_yaml_file')

    def handle(self, *args, **options):
        with open(options['merge_yaml_file']) as mergefile:
            merges = yaml.load(mergefile.read())
        for newCodeName, oldCodeNames in merges.items():
            code = Code(name=newCodeName)
            code.save()
            for oldCodeName in oldCodeNames:
                oldCode = Code.objects.get(name=oldCodeName)
                for a in oldCode.artifacts.all():
                    code.artifacts.add(a)
                oldCode.delete()
