from rest_framework import serializers
from codes.models import Code, Artifact

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('name', 'artifacts', 'id')
        read_only_fields = ('artifacts', "id")

class ArtifactSerializer(serializers.ModelSerializer):
    codes = serializers.PrimaryKeyRelatedField(many=True, queryset=Code.objects.all())

    class Meta:
        model = Artifact
        fields = ('text', 'codes', 'user_id', 'column_id')
        read_only_fields =  ('text', 'user_id', 'column_id')
