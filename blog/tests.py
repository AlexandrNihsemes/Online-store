from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import BlogPost


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class BlogPostViewsTest(TestCase):
    def setUp(self):
        self.published = BlogPost.objects.create(
            title="Опубликованная статья",
            content="Текст опубликованной статьи",
            is_published=True,
        )
        self.draft = BlogPost.objects.create(
            title="Черновик",
            content="Текст черновика",
            is_published=False,
        )

    def test_list_shows_only_published_posts(self):
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published.title)
        self.assertNotContains(response, self.draft.title)

    def test_detail_increments_views_count(self):
        response = self.client.get(reverse("blog:blog_detail", kwargs={"pk": self.published.pk}))
        self.assertEqual(response.status_code, 200)
        self.published.refresh_from_db()
        self.assertEqual(self.published.views_count, 1)

    def test_email_sent_at_100_views(self):
        self.published.views_count = 99
        self.published.save(update_fields=["views_count"])

        self.client.get(reverse("blog:blog_detail", kwargs={"pk": self.published.pk}))

        self.published.refresh_from_db()
        self.assertEqual(self.published.views_count, 100)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("100", mail.outbox[0].subject)

    def test_create_post(self):
        response = self.client.post(
            reverse("blog:blog_create"),
            {"title": "Новая статья", "content": "Содержимое", "is_published": "on"},
        )
        post = BlogPost.objects.get(title="Новая статья")
        self.assertRedirects(response, reverse("blog:blog_detail", kwargs={"pk": post.pk}))
        self.assertTrue(post.is_published)

    def test_update_redirects_to_post_detail(self):
        url = reverse("blog:blog_update", kwargs={"pk": self.published.pk})
        response = self.client.post(
            url,
            {"title": "Обновлённая статья", "content": "Новый текст", "is_published": "on"},
        )
        self.assertRedirects(response, reverse("blog:blog_detail", kwargs={"pk": self.published.pk}))
        self.published.refresh_from_db()
        self.assertEqual(self.published.title, "Обновлённая статья")

    def test_delete_post(self):
        response = self.client.post(reverse("blog:blog_delete", kwargs={"pk": self.draft.pk}))
        self.assertRedirects(response, reverse("blog:blog_list"))
        self.assertFalse(BlogPost.objects.filter(pk=self.draft.pk).exists())

    def test_str_and_meta(self):
        self.assertEqual(str(self.published), self.published.title)
        self.assertEqual(BlogPost._meta.verbose_name, "Запись блога")
        self.assertEqual(BlogPost._meta.verbose_name_plural, "Записи блога")
