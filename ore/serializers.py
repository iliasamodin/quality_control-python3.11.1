from rest_framework import serializers
from ore.models import Concentrate


class ConcentrateSerializer(serializers.ModelSerializer):
    """
    Serializer for individually adding and changing concentrate records 
    via the API.
    """

    class Meta:
        model = Concentrate
        fields = [
            "name", "year", "month", 
            "iron", "silicon", "aluminum", "calcium", "sulfur"
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "year": {"read_only": True},
            "month": {"read_only": True},
            "iron": {"required": False},
            "silicon": {"required": False},
            "aluminum": {"required": False},
            "calcium": {"required": False},
            "sulfur": {"required": False}
        }
