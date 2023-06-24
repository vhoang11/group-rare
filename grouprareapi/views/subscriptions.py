"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from grouprareapi.models import Post,Category,RareUser,Subscription


class SubscriptionView(ViewSet):
    """Level up game types view"""


    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Post.DoesNotExist:
          return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        subscription = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
 
       
        authId = RareUser.objects.get(uid=request.data["authorId"])
        followId = RareUser.objects.get(uid=request.data["followId"])
        

        subscription = Subscription.objects.create(
            created_on=request.data["createdOn"],
            ended_on=request.data["createdOn"],
            author_id=authId,
            follower_id=followId,
            
            
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)  
    
      
    
    def destroy(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author_id', 'follower_id',)
        depth = 1
