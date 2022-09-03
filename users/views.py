from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from .serializers import UserSerializer

# from .serializers import SimpleUserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


# class SimpleRegisterView(APIView):
#     """Register a user already active, without email verification needed"""

#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = SimpleUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         _ = serializer.save()
#         # I want the user to login afterwards, so I'll just
#         # return success message
#         return Response({"success": "User created successfully"})


class RegisterView(APIView):
    """
    Register user set as inactive at first,
    generate code to be sent to email for activation
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_token = default_token_generator.make_token(user)

        ### HERE I WOULD WANT TO START A BACKGROUND TASK TO SEND EMAIL WITH CODE AND USER ID ###
        # print("ID: ", user.id)
        # print("Token: ", confirmation_token)

        # I want the user to login afterwards, so I'll just
        # return success message
        return Response({"success": "User created successfully"})


class ActivateView(APIView):
    """
    Activate user with code sent to email
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Get the token from the url
        token = request.GET.get("token")
        # Get user id from url
        user_id = request.GET.get("user_id")

        # Get the user from the id
        User = get_user_model()
        user = User.objects.get(id=user_id)

        # Check if the token is not valid
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=400)

        # Activate the user
        user.is_active = True

        # Save the user
        user.save()

        return Response({"success": "User activated successfully"})
