from django.shortcuts import render
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LogoutAPIView(APIView):
    """
    API for logout.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        response_messages = {"message": "You are logged out"}
        return Response(response_messages)
