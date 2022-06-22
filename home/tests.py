from random import choices
from django.test import TestCase
from home.models import HomePage
from wagtail.models import Page


class HomePageTest(TestCase):
    def test_has_home_page(self):
        home_page = HomePage.objects.get(slug='home')
        self.assertEqual(home_page.slug, 'home')

    def test_can_create_home_page(self):
        home_page = HomePage.objects.get(slug='home')
        new_page = home_page.add_child(instance=HomePage(title='New Page', user_owner="1"))
        self.assertEqual(new_page.slug, 'new-page')
