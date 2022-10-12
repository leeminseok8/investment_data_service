from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class SignInSerializer(TokenObtainPairSerializer):
    """
    로그인 시리얼라이저
    비밀번호는 "0"으로 통일하여 제외하였습니다.
    """

    def validate(self, data):
        username = data.get("user_name")

        user = User.objects.get(user_name=username)

        token = super().get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return data
