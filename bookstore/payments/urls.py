from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^shoppingCart/', views.display_shopping_cart, name='shoppingCart'),
    url(r'^updateCart/', views.update_from_shopping_cart_page, name='updateShoppingCart'),
    url(r'^addBook/', views.add_book_to_cart, name='addBook'),
    url(r'^addFutureBook/', views.add_future_order_item, name='addFutureBookOrder'),
    url(r'^removeBook/$', views.remove_book_from_cart, name='deleteBook'),
    url(r'^removeFutureBook/(?P<book_id>\d+)/$', views.remove_future_order_item, name='deleteFutureBook'),
    url(r'^moveFutureBookToCart/(?P<book_id>\d+)/$', views.move_to_shopping_cart, name='moveFutureBookToCart'),
    url(r'^displayPaymentMethods/', views.display_credit_cards, name='displayCC'),
    url(r'^editCard/', views.manage_credit_card, name='manageCC'),
    url(r'^addCard/', views.CreditCardCreate.as_view(), name='addCC'),
    url(r'^deleteCard/', views.CreditCardDelete.as_view(), name='deleteCC'),
]
