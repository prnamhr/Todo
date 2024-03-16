from http.client import METHOD_NOT_ALLOWED
from django.http import HttpResponse
from rest_framework import generics
from .models import Comment, Task
from .serializers import CommentSerializer, TaskSerializer
from rest_framework.permissions import *
from .permissions import IsComment, IsOwnerOrReadOnly
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mainApp/todo_list.html'
    def get_queryset(self):
        queryset = Task.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return redirect('task-list-create')
        return Response(serializer.errors, status=400)
    def put(self, request, *args, **kwargs):
        raise METHOD_NOT_ALLOWED(method='PUT')

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mainApp/todo_detail.html'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsComment()] 
        else:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)
        comments = Comment.objects.filter(task=task)  
        return Response({'task': task, 'serializer': serializer, 'comments': comments}) 

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.get(request, *args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    def post(self, request, *args, **kwargs):
       
        task = self.get_object()
        mutable_data = request.data.copy()
        mutable_data['task'] = task.pk  
        serializer = CommentSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return redirect('task-detail', pk=task.pk)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return HttpResponse(status=204)
       
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj


class CommentDeleteAPIView(generics.DestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mainApp/comment_delete.html'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response({'comment': comment, 'serializer': serializer}) 
        
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return HttpResponse(status=204)