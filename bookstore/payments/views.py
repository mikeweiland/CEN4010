import decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView
from .forms import CreditCardForm
from products.models import Book
from .models import OrderItem, Order, CreditCard
from django.shortcuts import get_object_or_404


#########################################################################################################
##                                   CREDIT CARD FUNCTIONS                                            ##
########################################################################################################


def display_credit_cards(request):
    online_user = request.user
    cards = CreditCard.objects.filter(user_id=online_user.user_id)
    return render(request, 'payments/displayCreditCards.html', {'cards': cards})


class CreditCardCreate(CreateView):
    template_name = 'payments/addCreditCard.html'
    model = CreditCard
    form_class = CreditCardForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(CreditCardCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('payments:displayCC')


class CreditCardDelete(DeleteView):
    model = CreditCard
    success_message = 'Credit Card has been successfully removed.'

    def get_success_url(self):
        return reverse('payments:displayCC')

    def get_object(self):
        cc_id = self.request.POST.get('cc_id')
        return get_object_or_404(CreditCard, pk=cc_id)



@csrf_protect
def manage_credit_card(request):
    cc_id = request.POST.get("cc_id")
    cc = CreditCard.objects.get(pk=cc_id)
    form = CreditCardForm(request.POST or None, initial={'name_on_card': cc.name_on_card, 'cc_number': cc.cc_number,
                                                             'security_code': cc.security_code, 'expiration': cc.expiration})

    if request.method == 'POST':
        if form.is_valid():
            cc.name_on_card = form.cleaned_data['name_on_card']

    else:
        form = CreditCardForm(instance=cc)

    return render(request, 'payments/updateCreditCard.html', {'form': form})


#########################################################################################################
##                                   SHOPPING CART FUNCTIONS                                           ##
########################################################################################################

def display_shopping_cart(request):
    # get shopping cart id
    if 'orderId' in request.session:
        order_id = request.session['orderId']

    order_items = OrderItem.objects.filter(order_id=order_id)
    shopping_cart = Order.objects.filter(pk=order_id)
    return render(request, 'payments/shoppingCart.html', {'order_items': order_items, 'shopping_cart':shopping_cart})


def add_book_to_cart(request):
    # get parameters from quantity form
    quantity = request.POST.get('quantity')
    book_id = request.POST.get('bookId')
    next = request.POST.get('next', '/')

    # get book with id
    book = Book.objects.get(pk=book_id)
    price = book.price

    # get online user shopping cart id
    if 'orderId' in request.session:
        order_id = request.session['orderId']

    # find total price of quantity of specific book
    book_added_price = float(quantity) * float(price);

    # add order item to database
    add_book = OrderItem.objects.create(quantity=quantity, book_id=book_id, order_id=order_id,
                                        book_price_quantity=book_added_price)
    add_book.save()

    # update order price, tax price, and total price
    update_cart_price(order_id, book_added_price)

    return HttpResponseRedirect(next)


def remove_book_from_cart(request):
    order_item_id = request.GET.get('order_item_id')
    next = request.GET.get('next', '/')

    # get online user shopping cart id
    if 'orderId' in request.session:
        order_id = request.session['orderId']

    # get book item to remove from shopping cart
    book_order_item = get_object_or_404(OrderItem, pk=order_item_id)

    # update order total by removing price of books removed by the user
    update_remove_book_cart_price(book_order_item, order_id)

    book_order_item.delete()
    return HttpResponseRedirect(next)


def update_remove_book_cart_price(book_order_item, order_id):
    order = Order.objects.get(pk=order_id)

    # update price of order not including taxes
    order.price -= decimal.Decimal(book_order_item.book_price_quantity)

    # update tax price of order
    order.tax_price -= decimal.Decimal(book_order_item.book_price_quantity) * decimal.Decimal(0.07)

    # update total price of order
    order.total_price -= decimal.Decimal(book_order_item.book_price_quantity) \
                         + decimal.Decimal(book_order_item.book_price_quantity) * decimal.Decimal(0.07)

    order.save()


def update_from_shopping_cart_page(request):
    quantity = request.POST.get('quantity')
    order_item_id = request.POST.get('order_item_id')
    next = request.POST.get('next', '/')

    print(quantity)

    order_item = OrderItem.objects.get(pk=order_item_id)

    if quantity == order_item.quantity:
        print("The same shit!!!")
    else:
        print('Got something different!!!')

    return HttpResponseRedirect(next)


def update_cart_price(order_id, book_added_price):
    order = Order.objects.get(pk=order_id)

    # update price of order not including taxes
    order.price += decimal.Decimal(book_added_price)

    # update tax price of order
    order.tax_price += decimal.Decimal(book_added_price) * decimal.Decimal(0.07)

    # update total price of order
    order.total_price += decimal.Decimal(book_added_price) + decimal.Decimal(book_added_price) * decimal.Decimal(0.07)

    order.save()



