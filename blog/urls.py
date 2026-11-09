from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blog_list"),
    path("create/", views.BlogPostCreateView.as_view(), name="blog_create"),
    path("<int:pk>/", views.BlogPostDetailView.as_view(), name="blog_detail"),
    path("<int:pk>/edit/", views.BlogPostUpdateView.as_view(), name="blog_update"),
    path("<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="blog_delete"),
]
