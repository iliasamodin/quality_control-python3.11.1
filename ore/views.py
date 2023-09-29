from django.contrib.auth import logout
from ore.models import Concentrate
from django.core.exceptions import ObjectDoesNotExist
from ore.functions import (
    formatting_unique_key_of_concentrate,
    update_or_create_concentrate
)
from openpyxl import load_workbook

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

        serializer = update_or_create_concentrate(
            serializer_class=self.serializer_class,
            unique_key_of_concentrate=unique_key_of_concentrate,
            concentrate_data=request.data
        )

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


class UpdateConcentratesByTableAPIView(APIView):
    """
    Updating information for reports of concentrates 
    from a Excel file via API.
    """

    serializer_class = ConcentrateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response_messages = {
            "message": 
            "Pass an Excel file in .xlsx format with reports on concentrates"
        }
        return Response(response_messages)

    def post(self, request):
        if not request.user.has_perms([
            "ore.add_concentrate",
            "ore.change_concentrate"
        ]):
            response_messages = {
                "message": 
                "You cannot add or change information about concentrates"
            }
            return Response(response_messages)

        xlsx_file = request.FILES.get("file")
        # Checking whether the .xlsx file in the form 
        #   was transferred via the API
        if xlsx_file is None: 
            response_messages = {
                "message": 
                "The .xlsx file was not passed " \
                "under the corresponding 'file' key"
            }
            return Response(response_messages)

        # Obtaining a sheet with concentrates from an .xlsx file
        xlsx_of_concentrates = \
            iter(load_workbook(filename=xlsx_file)["Concentrates"])

        # Generating a list of sheet column names
        column_names_in_xlsx = []
        for cell in next(xlsx_of_concentrates):
            if cell.value is None:
                break
            column_names_in_xlsx.append(cell.value.lower())

        updated_reports_on_concentrates = []
        # Updating existing reports on concentrates 
        #   and adding new reports based on data from the .xlsx file
        for line in xlsx_of_concentrates:
            concentrate_data = {}
            # Formation of a dictionary with all concentrate data 
            #   obtained from the .xlsx file
            for i, cell in enumerate(line):
                if cell.value is None:
                    break
                concentrate_data.update({column_names_in_xlsx[i]: cell.value})

            unique_key_of_concentrate = formatting_unique_key_of_concentrate(
                concentrate_data["year"],
                concentrate_data["month"],
                concentrate_data["name"]
            )

            # Removing data of concentrate unique key 
            #   from its composition data
            del concentrate_data["year"], \
                concentrate_data["month"], \
                concentrate_data["name"]

            serializer = update_or_create_concentrate(
                serializer_class=self.serializer_class,
                unique_key_of_concentrate=unique_key_of_concentrate,
                concentrate_data=concentrate_data
            )

            # Generating a list of reports on concentrates 
            #   that have been updated or added 
            #   based on data from the .xlsx file, 
            #   to return this list in response to an API request
            updated_reports_on_concentrates.append(serializer.data)

        return Response(updated_reports_on_concentrates)
