from typing import Dict
from urllib.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

from .serializers import SignInSerializer


class SignInView(GenericAPIView):
    """
    JWT를 사용한 로그인 기능
    """

    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request: Request) -> Dict:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data
            return Response(
                {
                    "message": "로그인 되었습니다.",
                    "access_token": token["access"],
                    "refresh_token": token["refresh"],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
