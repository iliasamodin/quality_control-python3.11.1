# Converting types and formatting data of a composite unique key 
#   obtained from the request url into database data types
def formatting_unique_key_of_concentrate(year, month, concentrate_name):
    unique_data_of_concentrate = dict(
        name=concentrate_name.replace("-", " ").lower().capitalize(), 
        year=int(year), 
        month=int(month)
    )
    return unique_data_of_concentrate