from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer


class ContactView(APIView):
    """
    API view to handle contact requests.

    This view allows users to create a new contact request, retrieve
    a list of all contact requests, retrieve a specific contact request
    by its primary key, and delete contact requests.

    Methods:
        post(request):
            Allows users to create a new contact request.
            Expects contact information in the request body.

        get(request, pk=None):
            Retrieves contact requests. If `pk` is provided,
            retrieves a single contact request. Otherwise,
            retrieves a list of all contact requests.

        delete(request, pk=None):
            Deletes a specific contact request by its primary key if `pk`
            is provided. If no `pk` is provided, deletes all contact requests.

    Permissions:
        AllowAny:
            Any user can access this view regardless of authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Create a new contact request (email)"""
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Contact request received'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk=None):
        """Get contact(s) - single if pk provided, else all"""
        if pk is not None:
            contact = self._get_contact_or_none(pk)
            if not contact:
                return Response(
                    {'error': 'Contact not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ContactSerializer(contact)
            return Response(serializer.data)

        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete contact(s) - single if pk provided, else all"""
        if pk:
            contact = self._get_contact_or_none(pk)
            if not contact:
                return Response(
                    {'error': 'Contact not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            contact.delete()
            return Response(
                {'message': f'Contact {pk} deleted!'},
                status=status.HTTP_204_NO_CONTENT
            )

        Contact.objects.all().delete()
        return Response(
            {'message': 'All contacts deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

    def _get_contact_or_none(self, pk):
        """Internal helper: Returns Contact object or None"""
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return None
