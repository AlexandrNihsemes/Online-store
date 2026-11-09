from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import ProductForm
from .models import Contact, Product

PRODUCTS_PER_PAGE = 6


class HomeView(ListView):
    """Контроллер главной страницы: список товаров с постраничной навигацией."""

    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = PRODUCTS_PER_PAGE


class ProductDetailView(DetailView):
    """Контроллер страницы товара: получает pk, извлекает объект через ORM."""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Контроллер добавления товара: валидирует форму и сохраняет объект в БД."""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Товар «{self.object.name}» успешно добавлен.")
        return response

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})


class ContactsView(TemplateView):
    """
    Контроллер страницы контактов.
    Показывает контактные данные, заполненные в админке,
    и обрабатывает форму обратной связи.
    """

    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context.update(
            {
                "success": True,
                "name": request.POST.get("name", ""),
                "phone": request.POST.get("phone", ""),
                "message": request.POST.get("message", ""),
            }
        )
        return self.render_to_response(context)
