from django.test import TestCase, SimpleTestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from users import views

class TestStatusCodeGet(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.user = User()

    def test_login_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_get(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_register_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

class TestStatusCodeLoggedIn(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
    
    def test_login(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,reverse('weather:home'))

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'asdf5tgb'}
        User.objects.create_user(**self.credentials)
    
    def test_login_redirect_nonext(self):
        response = self.client.post(reverse('users:login'),self.credentials)
        #self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, '/')
    def test_login_redirect_next(self):
        response = self.client.post(reverse('users:login'),{'username': 'testuser',
            'password': 'asdf5tgb','next':reverse('users:login')})
        #self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response,reverse('users:login'))
