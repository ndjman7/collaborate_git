from django.contrib.auth import authenticate, login, logout
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from gram import settings
from .forms import SignupForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'member/login.html'
    success_url = 'photo:list'

    def get(self, request):
        self.context['form'] = LoginForm()
        return render(request, "member/login.html", self.context)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('photo:photo_list')
            else:
                return HttpResponse("Inactive user.")
        else:
            return redirect(settings.LOGIN_URL)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('photo:photo_list')


class LoginFormView(FormView):
    template_name = 'member/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('photo:photo_list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("Inactive user.")
        return super().form_valid(form)




        ###################################
        ############# Sign up #############
        ###################################

def signup(request):
    User = get_user_model()
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            img_profile = form.cleaned_data['img_profile']

            user = User.objects.create_user(
                username=username,
                password=password,
                img_profile=img_profile
            )

            login(request, user)
            return redirect('photo:photo_list')
        context['form'] = form
    else:
        context['form'] = SignupForm()

    return render(request, 'member/signup.html', context)