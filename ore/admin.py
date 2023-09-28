from django.contrib import admin
from ore.models import Concentrate


@admin.register(Concentrate)
class ConcentrateAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "month"]
    list_filter = ["name", "year", "month"]
