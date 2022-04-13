from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField()
