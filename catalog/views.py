from django.shortcuts import render

from .models import Contact, Product


def home(request):
    """
    Контроллер главной страницы.
    Выводит последние 5 созданных продуктов — в консоль и на страницу.
    """
    latest_products = Product.objects.select_related("category")[:5]

    print("Последние 5 продуктов:")
    for product in latest_products:
        print(f"  {product.name} — {product.price} руб. ({product.category.name})")

    return render(request, "home.html", {"products": latest_products})


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
            {"success": True, "name": name, "contact": contact},
        )

    return render(request, "contacts.html", {"contact": contact})
