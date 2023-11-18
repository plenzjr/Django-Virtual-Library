from rest_framework import generics, status, permissions
from rest_framework.response import Response

from app_account.apis import serializers as acc_serializers
from app_account.models import User


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view handles the creation of new users. It is open to all users,
    regardless of authentication status.
    """

    serializer_class = acc_serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handle POST request to create a new user.

        Args:
            request (Request): The incoming HTTP request containing user data.

        Returns:
            Response: A HTTP response with status code 201 and details of the created user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": acc_serializers.RegisterSerializer(
                    user,
                    context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            },
            status=status.HTTP_201_CREATED
        )


class ActiveUsersView(generics.ListAPIView):
    """
    API view to list all active users.

    This view requires the user to be an admin. It provides a list of users
    that are currently active.

    Attributes:
        serializer_class (UserSerializer): Specifies the serializer to be used.
        permission_classes (list): Defines the permissions required to access this view.
    """

    serializer_class = acc_serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """
        Get the active users.

        Returns:
            QuerySet: A QuerySet of active user instances.
        """

        return User.objects.active()


class AllUsersView(generics.ListAPIView):
    """
    API view to list all users, including inactive ones.

    This view requires the user to be an admin. It provides a list of all user
    instances, active and inactive.

    Attributes:
        serializer_class (UserSerializer): Specifies the serializer to be used.
        permission_classes (list): Defines the permissions required to access this view.
    """

    serializer_class = acc_serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """
        Get all user instances.

        Returns:
            QuerySet: A QuerySet of all user instances.
        """

        return User.objects.all_objects()
