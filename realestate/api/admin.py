from django.contrib import admin
from realestate.api.models import ApiKeys

class ApiKeysAdmin(admin.ModelAdmin):
    pass
admin.site.register(ApiKeys, ApiKeysAdmin)
