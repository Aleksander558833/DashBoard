from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm
from .models import OneTimeCode


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST['code']
            one_time_code = OneTimeCode.objects.get(code=code)
            user = one_time_code.user
            if user:
                user.is_active = True
                user.save()
                one_time_code.delete()
            else:
                return render(self.request, 'invalid_code.html')
        return redirect('account_login')