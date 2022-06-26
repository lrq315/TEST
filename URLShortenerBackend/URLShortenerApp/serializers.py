from rest_framework import serializers
from .models import User, URLShortenerResult


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class URLShortenerResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = URLShortenerResult
        fields = ['long_url', 'short_url']