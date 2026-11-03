from decimal import Decimal

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма добавления товара: все поля, кроме изображения, обязательны."""

    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")
        labels = {
            "name": "Наименование",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена, руб.",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например, Бот для Telegram с оплатой"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Что умеет товар"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("name", "description", "category", "price"):
            self.fields[field_name].required = True

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Укажите наименование товара.")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if not description:
            raise forms.ValidationError("Укажите описание товара.")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is None or price <= Decimal("0"):
            raise forms.ValidationError("Цена должна быть больше нуля.")
        return price
