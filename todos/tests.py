from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo
# Create your tests here.


class TodosAPITestCase(APITestCase):

    def create_todo(self):
        sample_todo={'title':'Hello','description':'Test'}
        response = self.client.post(reverse('todos'),sample_todo)

        return response

    def authenticate(self):
        self.client.post(reverse('register'),{
                        'username':'username',
                        'email':'email@test.com',
                        'password':'password'})
        response = self.client.post(
            reverse('login'),{'email':'email@test.com','password':'password'})
        
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

class TestListCreateTodos(TodosAPITestCase):


    def test_should_not_create_todo_with_no_auth(self):
        
        response = self.create_todo()
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_should__create_todo(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate()
        response = self.create_todo()
        self.assertEqual(Todo.objects.all().count(),previous_todo_count+1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],'Hello')
        self.assertEqual(response.data['description'],'Test')
    
    def test_retrives_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)

        
        self.create_todo()
        
        res=self.client.get(reverse('todos'))
        self.assertIsInstance(res.data['count'],int)
        self.assertEqual(res.data['count'],1)
    

class TestTodoDetailAPIView(TodosAPITestCase):

    def test_retrieves_one_item(self):
        self.authenticate()
        response = self.create_todo()
        resp = self.client.get(reverse('todo',kwargs={'id':response.data['id']}))
        self.assertEqual(resp.status_code,status.HTTP_200_OK)

        todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(todo.title,resp.data['title'])

        
    
    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_todo()
        update_data = {'title':'Hello','description':'Test Description','is_complete':True}
        resp = self.client.put(reverse('todo',kwargs={'id':response.data['id']}),update_data)
        self.assertEqual(resp.status_code,status.HTTP_200_OK)
        todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(todo.description,resp.data['description'])
        self.assertEqual(todo.is_complete,True)

    def test_deletes_one_item(self):
        self.authenticate()
        response = self.create_todo()
        prev_db_count = Todo.objects.all().count()

        self.assertGreater(prev_db_count,0)
        self.assertEqual(prev_db_count,1)

        resp = self.client.delete(reverse('todo',kwargs={'id':response.data['id']}))
        self.assertEqual(resp.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(),0)
        