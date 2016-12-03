from django.shortcuts import render
from rest_framework import viewsets, status
from codes.models import Code, Artifact
from codes.serializers import CodeSerializer, ArtifactSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import detail_route, list_route
from django.http import HttpResponse
import csv
import io

class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer

    @list_route(methods=['get'])
    def csv(self, request):
        users = {uid: {'user_id': uid} for uid in Artifact.user_ids()}
        for artifact in Artifact.objects.all():
            users[artifact.user_id].update(artifact.code_dict())

        output = io.StringIO()
        writer = csv.DictWriter(output, users[list(Artifact.user_ids())[0]].keys()) 
        writer.writeheader()
        for user, codes in users.items():
            writer.writerow(codes)
        output.seek(0)
        result = output.read()
        return HttpResponse(result, content_type="text/csv")

    @detail_route(methods=['get'])
    def code(self, request, pk):
        artifact = self.get_object()
        return render(request, 'codes/code.html', {
            'artifact': artifact,
            'artifact_codes': [c.id for c in artifact.codes.all()],
            'codes': [CodeSerializer(code).data for code in Code.objects.all()],
            'next_id': artifact.id + 1,
            'prev_id': artifact.id - 1
        })
