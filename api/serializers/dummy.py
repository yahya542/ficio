from rest_framework import serializers

class CSVUploadSchema(serializers.Serializer):
    file = serializers.FileField()