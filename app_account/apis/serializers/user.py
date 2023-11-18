from rest_framework import serializers

from app_account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the creation of new users. It ensures that the password
    field is write-only, ensuring it can't be retrieved after user creation.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.

        Args:
            validated_data (dict): The validated data for user creation.

        Returns:
            User: The newly created user instance.
        """

        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User objects.

    This serializer provides a way to convert User objects into a more easily
    consumable data structure for front-end applications. It also includes an
    additional uid field, which is read-only.

    Attributes:
        uid (UUIDField): Read-only field for user's UID.
    """

    uid = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            'uid',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
        ]
        read_only_fields = ['uid', 'is_active']
