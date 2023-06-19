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
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
          return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
 
       
        rUserId = RareUser.objects.get(pk=request.data["rareUserId"])
        catId = Category.objects.get(pk=request.data["categoryId"])

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

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.image_url=request.data["imageUrl"]
        post.content=request.data["content"]
        post.approved=request.data["approved"]
        category_id= Category.objects.get(pk=request.data["categoryId"])
        rare_user_id = RareUser.objects.get(pk=request.data["rareUserId"])
        
       

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content','approved','category_id', 'rare_user_id')
        depth = 1
