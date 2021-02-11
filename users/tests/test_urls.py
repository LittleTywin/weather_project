from django.test import SimpleTestCase

from django.shortcuts import reverse
from django.urls import resolve


class TestUrlsReverse(SimpleTestCase):
    def test_login(self):
        url = reverse('users:login')
        self.assertEqual(url, '/users/login/')
    def test_logout(self):
        url = reverse('users:logout')
        self.assertEqual(url, '/users/logout/')
    def test_register(self):
        url = reverse('users:register')
        self.assertEqual(url, '/users/register/')

class TestUrlsResolve(SimpleTestCase):
    def test_login(self):
        resolver = resolve('/users/login/')
        self.assertEqual(resolver.view_name, 'users:login')
    
    def test_logout(self):
        resolver = resolve('/users/logout/')
        self.assertEqual(resolver.view_name, 'users:logout')

    def test_register(self):
        resolver = resolve('/users/register/')
        self.assertEqual(resolver.view_name, 'users:register')
    
