from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


# Register the Contact model along with the ContactAdmin configuration
admin.site.register(Contact, ContactAdmin)
