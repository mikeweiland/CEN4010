import decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView
from .forms import CreditCardForm
from products.models import Book
from .models import OrderItem, Order, CreditCard, FutureOrderItem
from django.shortcuts import get_object_or_404
from django.contrib import messages


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
        messages.success(self.request, 'Credit Card has been successfully added.')
        return reverse('payments:displayCC')


class CreditCardDelete(DeleteView):
    model = CreditCard

    def get_success_url(self):
        messages.success(self.request, 'Credit Card has been successfully removed.')
        return reverse('payments:displayCC')

    def get_object(self):
        cc_id = self.request.POST.get('cc_id')
        return get_object_or_404(CreditCard, pk=cc_id)


@csrf_protect
def manage_credit_card(request):
    cc_id = request.GET.get("cc_id")
    cc = CreditCard.objects.get(pk=cc_id)
    form = CreditCardForm(request.POST or None, initial={'name_on_card': cc.name_on_card, 'cc_number': cc.cc_number,
                                                             'security_code': cc.security_code, 'expiration': cc.expiration})

    if request.method == 'POST':
        if form.is_valid():
            cc.name_on_card = form.cleaned_data['name_on_card']
            cc.cc_number = form.cleaned_data['cc_number']
            cc.security_code = form.cleaned_data['security_code']
            cc.expiration = form.cleaned_data['expiration']

            cc.save()

            messages.success(request, 'Credit Card was successfully updated.')

            return HttpResponseRedirect(reverse('payments:displayCC'))

    else:
        form = CreditCardForm(instance=cc)

    return render(request, 'payments/updateCreditCard.html', {'form': form})


#########################################################################################################
##                                   SHOPPING CART FUNCTIONS                                           ##
########################################################################################################

def display_shopping_cart(request):
    if request.session.get('orderId') != None:
        # get shopping cart id
        order_id = request.session['orderId']

        # get future cart id
        f_order_id = request.session['fOrderId']

        order_items = OrderItem.objects.filter(order_id=order_id)
        future_order_items = FutureOrderItem.objects.filter(future_order_id=f_order_id)
        shopping_cart = Order.objects.filter(pk=order_id)

        return render(request, 'payments/shoppingCart.html', {'order_items': order_items, 'shopping_cart': shopping_cart,
                                                          'future_order_items': future_order_items})
    return(request, '#' )

def add_book_to_cart(request):
    # get parameters from quantity form
    quantity = request.POST.get('quantity')
    book_id = request.POST.get('bookId')
    next = request.POST.get('next', '/')

    # get book with id
    book = Book.objects.get(pk=book_id)
    price = book.price

    # get online user shopping cart id
    order_id = request.session['orderId']

    # find total price of quantity of specific book
    book_added_price = float(quantity) * float(price)

    # add order item to database
    add_book = OrderItem.objects.create(quantity=quantity, book_id=book_id, order_id=order_id,
                                        book_price_quantity=book_added_price)
    add_book.save()

    # update order price, tax price, and total price
    update_cart_price(order_id, book_added_price)

    return HttpResponseRedirect(next)


def remove_book_from_cart(request):
    order_item_id = request.GET.get('order_item_id')

    # get online user shopping cart id
    order_id = request.session['orderId']

    # get book item to remove from shopping cart
    book_order_item = get_object_or_404(OrderItem, pk=order_item_id)

    # update order total by removing price of books removed by the user
    update_remove_book_cart_price(book_order_item, order_id)

    book_order_item.delete()
    return HttpResponseRedirect(reverse('payments:shoppingCart'))


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

    order_item = OrderItem.objects.get(pk=order_item_id)

    order_item.quantity = quantity

    order_item.save()

    return HttpResponseRedirect(reverse('payments:shoppingCart'))


def update_cart_price(order_id, book_added_price):
    order = Order.objects.get(pk=order_id)

    # update price of order not including taxes
    order.price += decimal.Decimal(book_added_price)

    # update tax price of order
    order.tax_price += decimal.Decimal(book_added_price) * decimal.Decimal(0.07)

    # update total price of order
    order.total_price += decimal.Decimal(book_added_price) + decimal.Decimal(book_added_price) * decimal.Decimal(0.07)

    order.save()


#########################################################################################################
##                                   FUTURE ORDER FUNCTIONS                                           ##
########################################################################################################

def add_future_order_item(request):

    f_order_id = request.session['fOrderId']

    book_id = request.POST.get('book_id')
    next = request.POST.get('next', '/')

    # check to see if book already exists in future order
    future_book_exists = FutureOrderItem.objects.filter(future_order_id=f_order_id, book_id=book_id)

    # if book already exists in future order don't add again, display error message
    if future_book_exists:
        messages.error(request, 'Book was already added to future order.')
    else:
        add_future_book = FutureOrderItem.objects.create(book_id=book_id, future_order_id=f_order_id)
        add_future_book.save()

        messages.success(request, 'Book was successfully added to future order.')

    return HttpResponseRedirect(next)


def remove_future_order_item(request, book_id):

    f_order_id = request.session['fOrderId']

    # get future book order item and the delete from database
    book_to_delete = get_object_or_404(FutureOrderItem, future_order_id=f_order_id, book_id=book_id)
    book_to_delete.delete()

    messages.success(request, 'Book was successfully removed from future order.')

    return HttpResponseRedirect(reverse('payments:shoppingCart'))


def move_to_shopping_cart(request, book_id):

    f_order_id = request.session['fOrderId']

    book = get_object_or_404(Book, pk=book_id)

    # get user shopping cart id
    order_id = request.session['orderId']

    # get future book order item and the delete from database
    book_to_delete = get_object_or_404(FutureOrderItem, future_order_id=f_order_id, book_id=book_id)
    book_to_delete.delete()

    # add book to shopping cart
    add_book = OrderItem.objects.create(quantity=1, book_id=book_id, order_id=order_id, book_price_quantity=book.price)
    add_book.save()

    # update order price, tax price, and total price
    update_cart_price(order_id, book.price)

    messages.success(request, 'Book was successfully moved to shopping cart.')

    return HttpResponseRedirect(reverse('payments:shoppingCart'))
