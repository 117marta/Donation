from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Institution, Donation
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError


class LandingPage(View):

    def bag_count_quantity(self):
        total = 0
        for bag in Donation.objects.all():
            total += bag.quantity
        return total

    def get(self, request):
        # bag_count = Donation.objects.all().count()
        institution_count = len(Institution.objects.all().distinct())  # bez duplikatów
        items = [Institution.objects.filter(type=1),
                 Institution.objects.filter(type=2),
                 Institution.objects.filter(type=3),
                 ]
        ctx = {
            'bag_count': self.bag_count_quantity,
            'institution_count': institution_count,
            'items': items,
        }
        return render(request, 'donation_app/index.html', context=ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, 'donation_app/form.html')


class Login(View):
    def get(self, request):
        return render(request, 'donation_app/login.html')


class Register(View):

    def get(self, request):
        return render(request, 'donation_app/register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email').casefold()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Hasła muszą być takie same!')
            return redirect('register')

        else:
            try:
                user = User.objects.create_user(
                    username=email,
                    first_name=name,
                    last_name=surname,
                    email=email,
                )
                user.set_password(password)  # aby zapisać jako zahaszowane hasło
                user.save()

                messages.success(request, 'Pomyślnie utworzono konto.')
                messages.success(request, 'Możesz się teraz zalogować.')
                return redirect('/login/')
            except IntegrityError:
                messages.error(request, 'Podany e-mail już istnieje!')
                return redirect('register')
