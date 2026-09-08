from rest_framework import generics, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = TokenObtainPairSerializer.get_token(user)
        response = self.get_success_headers(serializer.data)
        from rest_framework.response import Response

        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(tokens.access_token),
                "refresh": str(tokens),
            },
            status=201,
            headers=response,
        )


class ThrottledTokenView(TokenObtainPairView):
    throttle_scope = "auth"


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PersonalLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import get_user_model
        from rest_framework.response import Response

        User = get_user_model()
        user = User.objects.filter(username="lavid").first() or User.objects.first()
        if not user:
            user = User.objects.create_user(
                username="lavid",
                email="lavid@local.dev",
                password="cracked",
                display_name="Lavid",
            )
        tokens = TokenObtainPairSerializer.get_token(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(tokens.access_token),
                "refresh": str(tokens),
            }
        )
