from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from .forms import EditUserProfileForm, UserCreateForm
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from payments.models import Order


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

                # find the latest shopping cart by user
                latest_cart = Order.objects.filter(
                     user_id=current_user.user_id
                ).order_by('date_created').last()

                # check if latest cart exists or has already been purchased
                if latest_cart:

                    # create new shopping cart if latest cart has been payed
                    if latest_cart.payed_order:
                        new_cart = create_shopping_cart(current_user.user_id)
                        request.session['orderId'] = new_cart.id
                        return HttpResponseRedirect(next)

                    # use existing shopping cart that has not been payed for
                    # used when shoppers log off then log back in with preexisting shopping cart and books stored inside
                    else:
                        request.session['orderId'] = latest_cart.id
                        return HttpResponseRedirect(next)

                # create  new shopping cart for first time users
                else:
                    new_cart = create_shopping_cart(current_user.user_id)
                    request.session['orderId'] = new_cart.id
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


@csrf_protect
def manage_account(request):
    online_user = request.user
    form = EditUserProfileForm(request.POST or None, initial={'first_name': online_user.first_name,
                                                    'last_name': online_user.last_name, 'nickname': online_user.nickname,
                                                    'email_address': online_user.email_address})

    if request.method == 'POST':
        if form.is_valid():
            online_user.first_name = form.cleaned_data['first_name']
            online_user.last_name = form.cleaned_data['last_name']
            online_user.nickname = form.cleaned_data['nickname']
            online_user.email_address = form.cleaned_data['email_address']

            online_user.save()

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

