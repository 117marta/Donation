from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Institution, Donation
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
import datetime


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


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'
    # redirect_field_name = '/add_donation/'

    def get(self, request):
        institutions = Institution.objects.all()
        # categories = Category.objects.all().order_by('pk')
        categories = Category.objects.all()
        institution_categories = Institution.categories.through.objects.all()
        ctx = {'institutions': institutions, 'categories': categories, 'institution_categories': institution_categories}
        return render(request, 'donation_app/form.html', context=ctx)

    def post(self, request):
        user = request.user
        # chosen_categories = request.POST.getlist('categories')  # lista z nazwami kategorii
        # categories = Category.objects.filter(name__in=chosen_categories)
        # categories = request.POST.get('categories')

        categories = request.POST.getlist('categories')
        # institution = request.POST.get('organization')
        institution = Institution.objects.get(name=request.POST.get('organization'))
        quantity = request.POST.get('bags')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        pick_up_date = request.POST.get('pick_up_date')
        pick_up_time = request.POST.get('pick_up_time')
        pick_up_comment = request.POST.get('pick_up_comment')

        try:
            new_donation = Donation.objects.create(
                institution=institution,  # institution_id=institution
                quantity=quantity,
                address=address,
                city=city,
                zip_code=zip_code,
                phone_number=phone,
                pick_up_date=pick_up_date,
                pick_up_time=pick_up_time,
                pick_up_comment=pick_up_comment,
                user=user,
            )
            new_donation.categories.set(categories)
        # return redirect('confirmation')
            new_donation.save()
            return render(request, 'donation_app/form-confirmation.html')
        except Exception:
            messages.error(request, 'Coś poszło nie tak...')
            return redirect('add-donation')


class Login(View):

    def get(self, request):
        return render(request, 'donation_app/login.html')

    def post(self, request):
        try:
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Zalogowano!')
                return redirect('index')
            elif not User.objects.get(email=username).check_password(password):
                messages.error(request, 'Błędne hasło!')
                return redirect('login')
            else:
                messages.error(request, 'Błędne logowanie!')
                return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, 'Nie ma takiego użytkownika!')
            return redirect('register')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')


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


class Profile(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by('is_taken', 'date_taken', 'date_add')
        return render(request, 'donation_app/profile.html', {'donations': donations})


class DonationDetail(View):

    def get(self, request, id):
        donation = Donation.objects.get(pk=id)
        return render(request, 'donation_app/donation.html', {'donation': donation})

    def post(self, request, id):
        donation_id = request.POST.get('donation_id')
        status = request.POST.get('status')
        donation = Donation.objects.get(pk=donation_id)
        if status == 'taken':
            donation.is_taken = True
            now = datetime.datetime.now()
            donation.date_taken = now
            donation.save()
        else:
            donation.is_taken = False
            donation.save()
        return redirect('profile')
