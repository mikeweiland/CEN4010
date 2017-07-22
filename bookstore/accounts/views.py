from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DeleteView, CreateView
from payments.models import Order, FutureOrder
from .forms import EditUserProfileForm, UserCreateForm, AddressForm
from .models import User, Address
from django.contrib import messages


#########################################################################################################
##                                   USER FUNCTIONS                                                   ##
########################################################################################################

@csrf_protect
def login_view(request):

    if request.method == 'POST':
        username = request.POST['nickname']
        password = request.POST['password']
        next = request.POST.get('next', '/')

        user = authenticate(username=username, password=password)

        # if we have a user object, credentials correct
        if user:
            # check to see if account is active
            if user.is_active:
                # if account is active login the user and send the user back to homepage
                login(request, user)
                current_user = request.user

                try:
                    # find the latest shopping cart by user
                    latest_cart = Order.objects.filter(
                        user_id=current_user.user_id
                    ).order_by('date_created').last()

                    # create new shopping cart if latest cart has been payed
                    if latest_cart.payed_order:
                        new_cart = create_shopping_cart(current_user.user_id)
                        request.session['orderId'] = new_cart.id

                    # use existing shopping cart that has not been payed for
                    # used when shoppers log off then log back in with preexisting shopping cart and books stored inside
                    else:
                        request.session['orderId'] = latest_cart.id
                        
                except:
                    # create  new shopping cart if cart query fails
                    new_cart = create_shopping_cart(current_user.user_id)
                    request.session['orderId'] = new_cart.id

                try:
                    # find future order list of user
                    future_order_cart = FutureOrder.objects.get(
                        user_id=current_user.user_id
                    )

                    request.session['fOrderId'] = future_order_cart.id

                except:
                    # create  new shopping cart for first time users
                    new_future_order = create_future_order(current_user.user_id)
                    request.session['fOrderId'] = new_future_order.id

                return HttpResponseRedirect(next)

            # account is not active
            else:
                return HttpResponse("Your account has been disabled.")

        # no user with matching credentials
        else:
            # bad login credentials were provided
            return HttpResponse("Invalid login details supplied.")


# create cart for new users or customers with previous cart already purchased
def create_shopping_cart(user_id):
    o = Order.objects.create(user_id=user_id)
    o.save()
    return o


# create a future order for new users who login in to website
def create_future_order(user_id):
    future_order = FutureOrder.objects.create(user_id=user_id)
    future_order.save()
    return future_order


@csrf_protect
def manage_account(request):
    online_user = request.user
    user = User.objects.get(pk=online_user.user_id)
    form = EditUserProfileForm(request.POST or None, initial={'first_name': online_user.first_name,
                                                    'last_name': online_user.last_name, 'nickname': online_user.nickname,
                                                    'email_address': online_user.email_address}, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.nickname = form.cleaned_data['nickname']
            user.email_address = form.cleaned_data['email_address']

            user.save()

            messages.success(request, 'User information changes have been successfully saved.')

            return HttpResponseRedirect(reverse('index'))

    else:
        form = EditUserProfileForm(instance=online_user)

    return render(request, "accounts/manageAccount.html", {'form': form})


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("index")
    template_name = "accounts/signUp.html"


class LogoutView(generic.RedirectView):
    url = reverse_lazy("index")

    def get(self,request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


#########################################################################################################
##                                   ADDRESS FUNCTIONS                                                 ##
########################################################################################################

def display_address(request):
    online_user_id = request.user.user_id
    addresses = Address.objects.filter(user_id=online_user_id)
    return render(request, 'accounts/displayAddresses.html', {'addresses': addresses})


@csrf_protect
def update_address(request):
    addr_id = request.GET.get("addr_id")
    addr = Address.objects.get(pk=addr_id)
    form = AddressForm(request.POST or None, initial={'street_address': addr.street_address, 'city': addr.city,
                                                             'state': addr.state, 'zip_code': addr.zip_code})

    if request.method == 'POST':
        if form.is_valid():
            addr.street_address = form.cleaned_data['street_address']
            addr.city = form.cleaned_data['city']
            addr.state = form.cleaned_data['state']
            addr.zip_code = form.cleaned_data['zip_code']

            addr.save()

            messages.success(request, 'Address has been successfully updated.')

            return HttpResponseRedirect(reverse('accounts:displayAddress'))

    else:
        form = AddressForm(instance=addr)

    return render(request, 'accounts/updateAddress.html', {'form': form})


class AddressDelete(DeleteView):
    model = Address

    def get_success_url(self):
        messages.success(self.request, 'Address was successfully removed.')
        return reverse('accounts:displayAddress')

    def get_object(self):
        address_id = self.request.POST.get('addr_id')
        return get_object_or_404(Address, pk=address_id)


class AddressCreate(CreateView):
    template_name = 'accounts/addAddress.html'
    model = Address
    form_class = AddressForm

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.save()
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        messages.succcess(self.request, 'Address was successfully created.')
        return reverse('accounts:displayAddress')
