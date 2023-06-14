from django.shortcuts import render, redirect
from . import models
import telebot

bot = telebot.TeleBot("6269391112:AAFlxxKYVCaFS6l2BS26nmMATi3bSCoQ1hg")
from django.http import HttpResponse
# Create your views here.

def main_page(request):
    # Получение данных из базы
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()
    # Получение переменной из фронт части во время передачи
    search_value_from_front = request.GET.get("pr")
    if search_value_from_front:
        all_products = models.Product.objects.filter(name__contains=search_value_from_front)
    context = {"all_categories": all_categories, "all_products": all_products}
    # передача переменных на фронт
    return render(request, "index.html", context)
def get_category_products(request, pk):
    # получение товаров из конкретной категории
    exact_category_products = models.Product.objects.filter(category_name__id=pk)
    context = {"category_products": exact_category_products}
    return render(request, "category.html", context)
def get_products(request,name, pk):
    # получение товара
    product = models.Product.objects.get(name=name, id=pk)
    context = {"product": product}
    return render(request, "product.html", context)
def add_product_to_cart(request, pk):
    # получение выбранного количества товара из фронт части
    quantity = request.POST.get("pr_count")
    # найти сам продукт
    product_to_add = models.Product.objects.get(id=pk)
    models.UserCart.objects.create(user_id=request.user.id, user_product=product_to_add, user_product_quantity=quantity)
    return redirect("/")
def get_cart(request):
    user_id = request.user.id
    cart = models.UserCart.objects.filter(user_id=user_id)
    context = {"cart": cart}
    return render(request, "cart.html", context)
# Оформление заказа
def complete_order(request):
    user_cart=models.UserCart.objects.filter(user_id=request.user.id)
    # Сообщение в тг для админа

    if request.method == "POST":
        result_message = "Новый заказ(из Сайта)\n\n"
        total = 0
        for cart in user_cart:
            result_message += f"Название продукта: {cart.user_product}\n"\
                          f"Количество: {cart.user_product_quantity}\n\n"
            total += cart.user_product.price * cart.user_product_quantity
        result_message += f"\n\nИтог: {total}"
        bot.send_message(305896408, result_message)
        user_cart.delete()
        return redirect("/")
    return render(request, "user_cart.html", {"user_cart": user_cart})
def delete_from_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id=pk)
    models.UserCart.objects.filter(user_id=request.user.id, user_product=product_to_delete).delete()
    return redirect('/cart')