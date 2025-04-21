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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return None

    def delete(self, request, pk=None):
        if pk is not None:
            # Delete single contact
            contact = self.get_object(pk)
            if contact is None:
                return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

            if not request.user.is_staff:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            contact.delete()
            return Response({'message': 'Contact deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Delete all contacts
            if not request.user.is_staff:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            Contact.objects.all().delete()
            return Response({'message': 'All contacts deleted'}, status=status.HTTP_204_NO_CONTENT)
