from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Task, Comment

class BaseViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', description='Test Description', created_by=self.user)
        self.comment = Comment.objects.create(text='Test Comment', created_by=self.user, task=self.task)

class TaskListCreateAPIViewTests(BaseViewTest):
    def test_list_tasks(self):
        response = self.client.get(reverse('task-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'New Description'}
        response = self.client.post(reverse('task-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND) 
    def test_search_task(self):
        response = self.client.get(reverse('task-list-create') + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.task.title, str(response.content))
        
class TaskRetrieveUpdateDestroyAPIViewTests(BaseViewTest):

    def test_get_single_task(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_update_task(self):
        data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_post_comment(self):
        data = {'text': 'New Comment'} 
        self.task.refresh_from_db() 
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CommentDeleteAPIViewTests(BaseViewTest):
    def test_delete_comment(self):
        response = self.client.delete(reverse('comment-delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)