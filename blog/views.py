from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost

VIEWS_MILESTONE = 100


class BlogPostListView(ListView):
    """Список статей блога: только опубликованные записи."""

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Страница статьи: увеличивает счётчик просмотров и поздравляет на рубеже 100."""

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        BlogPost.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
        post.refresh_from_db(fields=["views_count"])

        if post.views_count == VIEWS_MILESTONE:
            send_mail(
                subject=f"Статья «{post.title}» достигла {VIEWS_MILESTONE} просмотров!",
                message=(
                    f"Поздравляем! Запись «{post.title}» набрала {post.views_count} просмотров.\n"
                    f"Ссылка на статью: {self.request.build_absolute_uri(post.get_absolute_url())}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.BLOG_NOTIFICATION_EMAIL],
                fail_silently=True,
            )

        return post


class BlogPostCreateView(CreateView):
    """Создание записи блога."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogPostUpdateView(UpdateView):
    """Редактирование записи блога с перенаправлением на её страницу."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление записи блога."""

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
