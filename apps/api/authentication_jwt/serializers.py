from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  AuthUser,
                                                  )

from rest_framework_simplejwt.tokens import Token



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user=user)

        token["id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["nickname"] = user.nickname
        token["is_active"] = user.is_active
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        token["is_trainer"] = user.is_trainer

        return token
