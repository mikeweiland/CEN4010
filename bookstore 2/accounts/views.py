from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from . import forms
from django.views import generic
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def LoginView(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['nickname']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # if we have a user object, credentials correct
        # else, no user with matching credentials
        if user:
            # check to see if account is active
            if user.is_active :
                # if account is active login the user and send the user back to homepage
                login(request,user)
                return HttpResponseRedirect('index')
            else:
                # account is not active
                return HttpResponse("Your account has been disabled.")
        else:
            # bad login credentials were provided
            return HttpResponse("Invalid login details supplied.")



class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("index")
    template_name = "accounts/signUp.html"

class LogoutView(generic.RedirectView):
    url = reverse_lazy("index")

    def get(self,request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)