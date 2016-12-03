from django.shortcuts import render
from rest_framework import viewsets, status
from codes.models import Code, Artifact
from codes.serializers import CodeSerializer, ArtifactSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import detail_route

class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer

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
