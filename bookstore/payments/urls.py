from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^shoppingCart/', views.display_shopping_cart, name='shoppingCart'),
    url(r'^shoppingCart/updateCart/', views.update_from_shopping_cart_page, name='updateShoppingCart'),
    url(r'^addBook/', views.add_book_to_cart, name='addBook'),
    url(r'^removeBook/$', views.remove_book_from_cart, name='deleteBook'),
    url(r'^displayPaymentMethods/',views.display_credit_cards, name='displayCC'),
    url(r'^displayPaymentMethods/editCard', views.manage_credit_card, name='manageCC'),
]