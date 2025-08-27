from rest_framework import serializers

class CSVUploadSchema(serializers.Serializer):
    file = serializers.FileField(help_text="CSV file containing the data to import")