from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма создания и редактирования записи блога."""

    class Meta:
        model = BlogPost
        fields = ("title", "content", "preview", "is_published")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например, «Как выбрать ноутбук»"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 10, "placeholder": "Текст статьи"}
            ),
            "preview": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
