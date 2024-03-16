from rest_framework import serializers
from .models import Task,Comment
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_by','created_at','updated_at']
class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'task', 'created_by', 'created_at', 'updated_at']