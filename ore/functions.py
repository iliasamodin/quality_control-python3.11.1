from ore.models import Concentrate
from django.core.exceptions import ObjectDoesNotExist


# Converting types and formatting data of a composite unique key 
#   obtained from the request url into database data types
def formatting_unique_key_of_concentrate(year, month, concentrate_name):
    unique_data_of_concentrate = dict(
        name=concentrate_name.replace("-", " ").lower().capitalize(), 
        year=int(year), 
        month=int(month)
    )
    return unique_data_of_concentrate


# Updating or creating a report on a concentrate, 
#   depending on whether there is a concentrate 
#   with a unique key passed to the function in the database
def update_or_create_concentrate(
    serializer_class, 
    unique_key_of_concentrate,
    concentrate_data
):

    # Changing an existing concentrate data report
    try:
        concentrate = Concentrate.objects.get(
            **unique_key_of_concentrate
        )
        serializer = serializer_class(
            instance=concentrate,
            data=concentrate_data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    # Adding a report with concentrate data
    except ObjectDoesNotExist:
        serializer = serializer_class(data=concentrate_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**unique_key_of_concentrate)

    return serializer
