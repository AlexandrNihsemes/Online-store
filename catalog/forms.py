from decimal import Decimal
from pathlib import Path

from django import forms

from .constants import (
    ALLOWED_IMAGE_CONTENT_TYPES,
    ALLOWED_IMAGE_EXTENSIONS,
    FORBIDDEN_WORDS,
    MAX_IMAGE_SIZE,
)
from .models import Product


def find_forbidden_words(value: str) -> list[str]:
    """Возвращает запрещённые слова, найденные в тексте (без учёта регистра)."""

    normalized = value.casefold()
    return [word for word in FORBIDDEN_WORDS if word in normalized]


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования товара с валидацией и стилизацией полей."""

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ("name", "description", "category", "price"):
            self.fields[field_name].required = True

        self.fields["name"].widget.attrs["placeholder"] = "Например, «Бот для Telegram с оплатой»"
        self.fields["description"].widget.attrs["placeholder"] = "Что умеет товар"
        self.fields["price"].widget.attrs["placeholder"] = "0.00"
        self.fields["image"].help_text = "Форматы JPEG или PNG, размер файла не больше 5 МБ."

        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = "form-select"
            elif isinstance(widget, (forms.Textarea, forms.FileInput)):
                widget.attrs["class"] = "form-control"
                if isinstance(widget, forms.Textarea):
                    widget.attrs["rows"] = 4
            else:
                widget.attrs["class"] = "form-control"

        self.fields["image"].widget.attrs["accept"] = "image/jpeg,image/png"
        self.fields["price"].widget.attrs.update({"min": "0", "step": "0.01"})

    def _check_forbidden_words(self, value: str, field_label: str) -> None:
        found = find_forbidden_words(value)
        if found:
            words = ", ".join(f"«{word}»" for word in found)
            raise forms.ValidationError(
                f"{field_label}: нельзя использовать запрещённые слова — {words}. "
                "Уберите их из текста и сохраните форму ещё раз."
            )

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Укажите название товара — без него карточку не сохранить.")
        self._check_forbidden_words(name, "Наименование")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if not description:
            raise forms.ValidationError("Укажите описание товара — без него карточку не сохранить.")
        self._check_forbidden_words(description, "Описание")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is None:
            raise forms.ValidationError("Укажите цену товара числом, например 1990.00.")
        if price < 0:
            raise forms.ValidationError(
                f"Цена не может быть отрицательной: вы указали {price}. "
                "Введите нулевое или положительное значение, например 1990.00."
            )
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image or not hasattr(image, "content_type"):
            # Поле не заполнено или осталось прежнее изображение товара.
            return image

        extension = Path(image.name).suffix.lower()
        if extension not in ALLOWED_IMAGE_EXTENSIONS or image.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise forms.ValidationError(
                "Недопустимый формат файла. Загрузите изображение в формате JPEG или PNG."
            )

        if image.size > MAX_IMAGE_SIZE:
            size_mb = image.size / (1024 * 1024)
            raise forms.ValidationError(
                f"Файл слишком большой: {size_mb:.1f} МБ. "
                "Загрузите изображение размером не больше 5 МБ."
            )

        return image
