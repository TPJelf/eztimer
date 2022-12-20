from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django.apps import apps

# user model - showing all fields in list except password and relations

admin.site.unregister(User)

field_names = [field.name for field in User._meta.get_fields() if not field.is_relation and field.name != 'password']
class UserAdmin(admin.ModelAdmin):
    list_display = field_names

admin.site.register(User, UserAdmin)

# tz with calc offset

class TimezoneAdmin(admin.ModelAdmin):
  list_display = ['name', 'utc_offset']

admin.site.register(Timezone, TimezoneAdmin)

# all other models - showing all fields except relations

class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

models = apps.get_models()
for model in models:
    try:
        admin.site.register(model, UniversalAdmin)
    except admin.sites.AlreadyRegistered:
        pass