"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from grouprareapi.models import Post,Category,RareUser


class PostView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = Event.objects.get(pk=pk)
            serializer = EventSerializer(game_type)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        
        game_type = request.query_params.get('game', None)
        if game_type is not None:
          events = events.filter(game_id=game_type)
        
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)

        for event in events:
            # Check to see if there is a row in the Event Games table that has the passed in gamer and event
            event.joined = len(EventGamer.objects.filter(
                gamer=gamer, event=event)) > 0
  
          
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
 
       
        rUserId = RareUser.objects.get(pk=request.data["rare_user_id"])
        catId = Category.objects.get(pk=request.data["category_id"])

        post = Post.objects.create(
            title=request.data["title"],
            publication_date=request.data["publicationDate"],
            image_url=request.data["imageUrl"],
            content=request.data["content"],
            approved=request.data["approved"],
            category_id=catId,
            rare_user_id = rUserId
            
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        event = Event.objects.get(pk=pk)
        event.game = Game.objects.get(pk=request.data["game"])
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        organizer= Gamer.objects.get(uid=request.data["userId"])

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """DELETE request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.get(
            gamer=gamer,
            event=event
        )
        attendee.delete()
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content','approved','category_id', 'rare_user_id')
        depth = 1
