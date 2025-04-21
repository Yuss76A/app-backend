from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer


class ContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contact request received'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):  # Add pk parameter here
        if pk is not None:
            # Handle single contact retrieval
            contact = self.get_object(pk)
            if contact is None:
                return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        else:
            # Handle list of contacts
            contacts = Contact.objects.all()
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return None

    # Delete emails (admin only)
    def delete(self, request, pk=None):
        if pk:
            # Delete single email
            email = self._get_email_or_404(pk)
            email.delete()
            return Response(
                {'message': f'Email {pk} deleted!'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            # Delete ALL emails (use with caution!)
            Contact.objects.all().delete()
            return Response(
                {'message': 'All emails deleted!'}, 
                status=status.HTTP_204_NO_CONTENT
            )

    # Helper method to find email or return 404
    def _get_email_or_404(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response(
                {'error': 'Email not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
