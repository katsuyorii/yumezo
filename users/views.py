from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, redirect

from django.views.generic import FormView, TemplateView, View, UpdateView, ListView

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.tokens import default_token_generator

from django.urls import reverse_lazy

from django.utils.http import urlsafe_base64_decode

from .forms import LoginUserForm, RegistrationUserForm, ChangePasswordUserForm, EditInfoUserForm
from .models import User
from .tasks import activate_email_task

from catalog.models import Favorites


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
        activate_email_task.delay(user.pk)
        
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
            activate_email_task.delay(self.request.user.pk)
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
    

'''
    Класс-представление для обработки логики подтверждения токена пользователя и активация пользователя
'''
class ActivateEmailCheckView(View):  
    def get(self, request, uidb64, token):  
        try:  
            uid = urlsafe_base64_decode(uidb64)  
            user = User.objects.get(pk=uid)  
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and default_token_generator.check_token(user, token):  
            user.is_active = True
            user.save()  
            login(request, user)  
            return HttpResponseRedirect(reverse_lazy('activate_email_confirm'))
        else:  
            return HttpResponseRedirect(reverse_lazy('activate_email_not_confirm'))
        

'''
    Класс-представление для страницы подтверждения активации учетной записи
'''
class ActivateEmailConfirmView(TemplateView):
    template_name = 'users/activate-email-confirm.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Подтверждение E-mail'

            return context
    

'''
    Класс-представление для страницы ошибки активации учетной записи
'''
class ActivateEmailErrorView(TemplateView):
    template_name = 'users/activate-email-not-confirm.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Подтверждение E-mail'

            return context
    

'''
    Класс-представление для повторной отправки на email
'''
class ActivateEmailRepeatSendView(View):
    def get(self, request): 
        activate_email_task.delay(request.user.pk)
        return HttpResponseRedirect(reverse_lazy('activate_email_done'))
    

'''
    Класс-представление для страницы с избранными товарами пользователя
'''
class FavoritesUserView(ListView):
    model = Favorites
    template_name = 'users/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        queryset = Favorites.objects.filter(user=self.request.user).select_related('product__category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Избранное'

        return context
    

'''
    Класс-представление для удаления из избранного
'''
class FavoritesDeleteUserView(View):
    def get(self, request, *args, **kwargs):
        favor = get_object_or_404(Favorites, pk=self.kwargs['favorites_id'])
        favor.delete()

        messages.success(request, 'Товар удален из изранного!')
        return redirect(reverse_lazy('favorites'))