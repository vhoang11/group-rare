"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grouprareapi.models import RareUser

class RareUserView(ViewSet):
    """Rare Users view"""
    
    def list(self, request):
        """Handle GET requests to get all users
        Returns:
            Response -- JSON serialized list of users
        """
        rare_user = RareUser.objects.all()
        serializer = RareUserSerializer(rare_user, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
      try:
        rare_user = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)
      except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def update(self, request, pk):
        rare_user = RareUser.objects.get(pk=pk)
        rare_user.first_name = request.data["first_name"]
        rare_user.last_name = request.data["last_name"]
        rare_user.bio = request.data["bio"]
        rare_user.profile_image_url=request.data["profile_image_url"]
        rare_user.created_on = request.data["created_on"]
        rare_user.email=request.data["email"]
        
        rare_user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = RareUser
        fields = ('id', 'first_name', 'last_name', 'bio', 'profile_image_url', 'created_on', 'email', 'uid')
        depth = 1
