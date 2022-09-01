from django.contrib import admin
from .models import SampleModel


class SampleModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SampleModel, SampleModelAdmin)
