from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False,
        allow_empty=True,
    )
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'password_confirm',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'profile_picture',
            'phone_number',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'groups',
            'user_permissions',
        ]
        read_only_fields = ['id', 'last_login', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        groups = validated_data.pop('groups', []) 
        user_permissions = validated_data.pop('user_permissions', [])

        user = self.Meta.model(**validated_data)

        if password:
            if password != password_confirm:
                raise serializers.ValidationError("Passwords do not match.")
            user.set_password(password)

        user.save()

        if user_permissions:
            user.user_permissions.set(user_permissions)

        if groups:
            user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        groups = validated_data.pop('groups', None)
        permissions = validated_data.pop('user_permissions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            if password != password_confirm:
                raise serializers.ValidationError("Passwords do not match.")
            instance.set_password(password)

        instance.save()

        if permissions is not None:
            instance.user_permissions.set(permissions)

        if groups is not None:
            instance.groups.set(groups)

        return instance