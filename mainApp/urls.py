from django.urls import path,reverse_lazy
from .views import *

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/delete', CommentDeleteAPIView.as_view(), name='comment-delete'),
]
