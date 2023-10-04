from django.contrib import admin
from ore.models import Concentrate


@admin.register(Concentrate)
class ConcentrateAdmin(admin.ModelAdmin):
    list_display = ["name", "batch", "year", "month"]
    list_filter = ["name", "batch", "year", "month"]
