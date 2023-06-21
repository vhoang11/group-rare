from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from grouprareapi.models import Comment, RareUser, Post
from datetime import datetime

class CommentView(ViewSet):
    """Comment view set"""
    def create(self, request):
        """CREATE Comment
        """
        author_id = RareUser.objects.get(pk=request.data["author_id"])
        post_id = Post.objects.get(pk=request.data["post_id"])
        created_on = datetime.strptime(request.data["created_on"], "%B %d, %Y, %I:%M%p")
        comment = Comment.objects.create(
            author_id=author_id,
            post_id=post_id,
            content=request.data["content"],
            created_on=created_on,
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        """GET Single Comment"""
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """GET All Comments"""
        post_id = request.query_params.get('postId', None)
        comments = Comment.objects.all().filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """UPDATE Comment"""
        comment = Comment.objects.get(pk=pk)
        comment.author_id = RareUser.objects.get(pk=request.data["author_id"])
        comment.post_id_id = Post.objects.get(pk=request.data["post_id"])
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.save()
        return Response('Comment edited', status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        """DELETE Comment"""
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response('Comment deleted', status=status.HTTP_204_NO_CONTENT)
    
class CommentSerializer(serializers.ModelSerializer):
    """JSON Serializer for comments"""
    created_on = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")
    class Meta:
        model = Comment
        fields = ('id', 'author_id', 'post_id', 'content', 'created_on')
