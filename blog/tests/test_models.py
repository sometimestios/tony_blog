from django.apps import apps
from django.test import TestCase
from ..models import Post, Category, Tag
from django.contrib.auth.models import User
from django.shortcuts import reverse
import time

class PostModelTestCase(TestCase):
    def setUp(self):
        # apps.get_app_configs('haystack').signal_processor.teardown()
        user = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin',
        )
        cate = Category.objects.create(
            name='测试类'
        )
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)
        old_post_modified_time = self.post.modified_time
        time.sleep(2)
        self.post.body = "新的正文内容"
        self.post.save()
        self.post.refresh_from_db()
        # print(self.post.modified_time)
        # print(old_post_modified_time)
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 400)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})

        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)
