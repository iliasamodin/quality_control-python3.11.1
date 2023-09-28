from django.contrib.auth import logout
from ore.models import Concentrate
from django.core.exceptions import ObjectDoesNotExist
from ore.functions import formatting_unique_key_of_concentrate

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ore.serializers import ConcentrateSerializer


class LogoutAPIView(APIView):
    """
    API for logout.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        response_messages = {"message": "You are logged out"}
        return Response(response_messages)


class ConcentrateAPIView(APIView):
    """
    API view for viewing and adding data 
    on the quality indicators of the concentrate.
    """

    queryset = Concentrate.objects.all()
    serializer_class = ConcentrateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month, concentrate_name):
        # If the user does not have permission to view concentrate data, 
        #   then the user will receive a corresponding message 
        #   in response to the request
        if not request.user.has_perm("ore.view_concentrate"):
            response_messages = {
                "message": 
                "You cannot view information about concentrates"
            }
            return Response(response_messages)

        try:
            queryset = self.queryset.get(
                **formatting_unique_key_of_concentrate(
                    year, 
                    month, 
                    concentrate_name
                )
            )
            concentrate = self.serializer_class(instance=queryset).data
            return Response(concentrate)

        except ObjectDoesNotExist:
            response_messages = {
                "message": 
                "The report for the specified date " \
                "has not yet been completed " \
                "for the concentrate with this name. " \
                "To fill out the report, send the percentage of " \
                "'iron', 'silicon', 'aluminum', 'calcium' and 'sulfur' " \
                "content in a post request to the current page."
            }
            return Response(response_messages)

    def post(self, request, year, month, concentrate_name):
        if not request.user.has_perms([
            "ore.add_concentrate",
            "ore.change_concentrate"
        ]):
            response_messages = {
                "message": 
                "You cannot add or change information about concentrates"
            }
            return Response(response_messages)

        unique_key_of_concentrate = formatting_unique_key_of_concentrate(
            year, 
            month, 
            concentrate_name
        )

        # Changing an existing concentrate data report
        try:
            concentrate = Concentrate.objects.get(**unique_key_of_concentrate)
            serializer = self.serializer_class(
                instance=concentrate,
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # Adding a report with concentrate data
        except ObjectDoesNotExist:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(**unique_key_of_concentrate)

        return Response(serializer.data)


class DeleteConcentrateAPIView(APIView):
    """
    Deleting a report of concentrate for year and month from the url.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, year, month, concentrate_name):
        if not request.user.has_perm("ore.delete_concentrate"):
            response_messages = {
                "message": 
                "You cannot delete concentrates"
            }
            return Response(response_messages)
        
        try:
            concentrate = Concentrate.objects.get(
                **formatting_unique_key_of_concentrate(
                    year, 
                    month, 
                    concentrate_name
                )
            )
            concentrate.delete()
            
            response_messages = {"message": "Concentrate report deleted"}

        except ObjectDoesNotExist:
            response_messages = {
                "message": 
                "There is no report for the concentrate with this name " \
                "for the specified date in the database"
            }

        return Response(response_messages)
