from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Contact model.

    This class customizes the Django admin interface for the Contact
    model, allowing administrators to manage contact requests easily.

    Attributes:
        list_display (tuple): Fields to be displayed in the list view
        of the admin interface, helping administrators quickly see
        relevant contact information.

        search_fields (tuple): Fields that can be searched in the admin
        interface, enabling administrators to find contact requests
        by name or email.
    """
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


admin.site.register(Contact, ContactAdmin)
