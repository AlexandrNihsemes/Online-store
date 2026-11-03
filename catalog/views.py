from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Contact, Product

PRODUCTS_PER_PAGE = 6


def home(request):
    """Контроллер главной страницы: список товаров с постраничной навигацией."""
    products = Product.objects.all()

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "home.html", {"products": page_obj, "page_obj": page_obj})


def product_detail(request, pk):
    """Контроллер страницы товара: получает pk, извлекает объект через ORM."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def product_add(request):
    """Контроллер добавления товара: валидирует форму и сохраняет объект в БД."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Товар «{product.name}» успешно добавлен.")
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "product_form.html", {"form": form})


def contacts(request):
    """
    Контроллер страницы контактов.
    Показывает контактные данные, заполненные в админке,
    и обрабатывает форму обратной связи.
    """
    contact = Contact.objects.first()

    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")

        return render(
            request,
            "contacts.html",
            {"success": True, "name": name, "contact": contact, "phone": phone, "message": message},
        )

    return render(request, "contacts.html", {"contact": contact})
