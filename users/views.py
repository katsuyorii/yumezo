from django.http import HttpResponseRedirect

from django.shortcuts import redirect

from django.views.generic import FormView, TemplateView, View, UpdateView

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy

from .forms import LoginUserForm, RegistrationUserForm, ChangePasswordUserForm, EditInfoUserForm
from .models import User


'''
    Класс-представление для авторизации пользователей
'''
class LoginUserView(FormView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form): 
        user = form.cleaned_data['user']
        
        login(self.request, user)

        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка авторизации!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context


'''
    Класс-представление для регистарции новых пользователей
'''
class RegistrationUserView(FormView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse_lazy('activate_email_done')

    def form_valid(self, form): 
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']

        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)
        login(self.request, user)
        
        messages.success(self.request, 'Вы зарегестрировались в системе!')
        return super().form_valid(form)
            
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка регистрации!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Регистрация'

            return context
    

'''
    Класс-представление для профилей пользователей
'''
class ProfileUserView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Мой профиль'

            return context
    

'''
    Класс-представление для выхода из профиля
'''
class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы!')
        return redirect(reverse_lazy('index'))
    

'''
    Класс-представление для смены пароля
'''
class ChangePasswordUserView(PasswordChangeView):
    template_name = 'users/change-password.html'
    form_class = ChangePasswordUserForm

    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно сменили пароль!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка заполнения формы!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'

        return context
    

'''
    Класс-представление для редактирования информации профиля
'''
class EditInfoUserView(UpdateView):
    model = User
    form_class = EditInfoUserForm
    template_name = 'users/profile-edit.html'

    def form_valid(self, form):
        current_email = User.objects.get(pk=self.request.user.pk)
        new_email = form.cleaned_data['email']
        messages.success(self.request, 'Вы успешно редактировали профиль!')
        
        if current_email.email == new_email:
            return super().form_valid(form)
        else:
            self.object = form.save(commit=False)
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('activate_email_done'))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка заполнения формы!')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

    # Переопределние метода, чтобы не указывать pk или slug в url
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'

        return context
    

'''
    Класс-представление для страницы ожидания активации учетной записи
'''
class ActivateEmailDoneView(TemplateView):
    template_name = 'users/activate-email-done.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Подтверждение E-mail'

            return context