from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Institution, Donation
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from .forms import SignupForm, RemindPasswordForm, ResetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse


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

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        message = request.POST.get('message')
        email_subject = f'Wiadomość od {request.user}. ' \
                        f'{name} {surname} wysłał/a właśnie wiadomość przez formularz kontaktowy.'
        superusers = User.objects.filter(is_superuser=True)
        for sup_user in superusers:
            contact_email = EmailMessage(
                subject=email_subject,
                body=message,
                to=[sup_user.email],
                headers={'Reply-To': 'example@mail.pl', 'bcc': 'ukryte_do_wiadomosci@gmail.com', 'cc': 'kopia@op.pl'},
            )
            contact_email.send(fail_silently=False)

        messages.success(request, f'Wiadomość została wysłana. Dziękujemy {name.capitalize()} za kontakt!')
        return redirect('index')


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

        categories = request.POST.getlist('categories')
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
            username = request.POST.get('email').casefold()
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


# PasswordTokenGenerator - class that is used to reset the password
# In the above code, we generated the unique token for confirmation
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

account_activation_token = TokenGenerator()


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
                # user.save()
                # messages.success(request, 'Pomyślnie utworzono konto.')
                # messages.success(request, 'Możesz się teraz zalogować.')
                # return redirect('/login/')


                # Potwierdzenie/aktywacja konta
                user.is_active = False  # użytkownik nie zaloguje się, dopóki nie potwierdzi adresu e-mail
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Aktywuj swoje konto!'
                message = render_to_string('donation_app/activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(mail_subject, message, to=[email])
                email.send()
                messages.success(request, 'Potwierdź adres e-mail, aby dokończyć rejestrację.')
                return render(request, 'donation_app/signup.html')


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


class ProfileSettings(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'donation_app/profile-settings.html')

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        new_first_name = request.POST.get('new_first_name')
        new_last_name = request.POST.get('new_last_name')
        new_email = request.POST.get('new_email').casefold()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if 'new_info' in request.POST:
            if not password or not password2:
                messages.error(request, 'Do potwierdzenia zmian wpisz hasło')
                return redirect('settings')
            if password != password2:
                messages.error(request, 'Hasła różnią się od siebie')
                return redirect('settings')
            if user.check_password(password) is False:
                messages.error(request, 'Nieprawidłowe hasło')
                return redirect('settings')

            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.save()
            messages.success(request, 'Pomyślnie zmieniono dane')
            return render(request, 'donation_app/profile-settings.html')

        if 'new_pass' in request.POST:
            old_password = request.POST.get('old_password')
            if old_password:
                if user.check_password(old_password) is True:
                    new_password = request.POST.get('new_password')
                    new_password2 = request.POST.get('new_password2')
                    if new_password == new_password2:
                        user.set_password(new_password)
                        user.save()
                        login(request, user=user)
                        messages.success(request, 'Pomyślnie zmieniono hasło')
                        return redirect('settings')
                    else:
                        messages.error(request, 'Hasła różnią się od siebie')
                        return redirect('settings')
                else:
                    messages.error(request, 'Wprowadzono błędne hasło')
                    return redirect('settings')
            else:
                messages.error(request, 'Wpisz stare hasło')
                return redirect('settings')


# class Signup(View):
#
#     def get(self, request):
#         form = SignupForm()
#         return render(request, 'donation_app/signup.html', {'form': form})
#
#     def post(self, request):
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=True)  # zapisanie formularza w pamięci, nie w BD
#             user.is_active = False  # użytkownik nie zaloguje się, dopóki nie potwierdzi adresu e-mail
#             user.save()
#
#             current_site = get_current_site(request)
#             mail_subject = 'Aktywuj swoje konto!'
#             message = render_to_string('donation_app/activate_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user)
#             })
#             to_email = form.cleaned_data.get('email').casefold()
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             messages.success(request, 'Potwierdź adres e-mail, aby dokończyć rejestrację.')
#             return render(request, 'donation_app/signup.html', {'form': form})
#         else:
#             messages.error(request, 'Wystąpił błąd.')
#             return render(request, 'donation_app/signup.html', {'form': form})


class Activation(View):  # sprawdza prawidłowość tokena, a później pozwala na aktywację użytkownika i zalogowanie

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True  # użytkownik może się zalogować
            user.save()
            # login(request, user)  # automatyczne zalogowanie po kliknięciu w link aktywacyjny
            messages.success(request, 'Dziękujemy za potwierdzenie adresu e-mail.')
            messages.success(request, 'Możesz się teraz zalogować.')
            return redirect('index')
        else:
            messages.error(request, 'Link aktywacyjny jest nieprawidłowy.')
            return redirect('index')


class RemindPasswordView(View):

    def get(self, request):
        form = RemindPasswordForm()
        return render(request=request, template_name='donation_app/remind-password.html', context={'form': form})

    def post(self, request):
        form = RemindPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].casefold()
            try:
                user = User.objects.get(email=email)
            except Exception:
                user = None

            if user:
                current_site = get_current_site(request)
                mail_subject = 'Resetuj hasło'
                message = render_to_string(
                    template_name='donation_app/reset-password.html',
                    context={
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }
                )
                email = EmailMessage(subject=mail_subject, body=message, to=[email])
                email.send()
                messages.success(request=request, message='Na podany adres e-mail wysłano link do zresetowania hasła.')
                return redirect('remind-password')
            else:
                form = RemindPasswordForm()
                messages.error(request=request, message='Nie ma takiego konta w bazie!')
                return render(
                    request=request,
                    template_name='donation_app/remind-password.html',
                    context={'form': form},
                )

        # messages.error(request=request, message='Błąd w formularzu!')
        # return render(
        #             request=request,
        #             template_name='donation_app/remind-password.html',
        #             context={'form': form},
        #         )


class ResetPassword(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            form = ResetPasswordForm()
            messages.success(request, 'Twoje hasło zostanie zresetowane.')
            return render(request=request, template_name='donation_app/change-password.html', context={'form': form})
        else:
            messages.error(request, 'Link aktywacyjny jest nieprawidłowy.')
            return redirect('reset-password')

    def post(self, request, uidb64, token):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            password = request.POST['new_password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Pomyślnie zmieniono hasło! Możesz się teraz zalogować.')
            # login(request=request, user=user)  # automatyczne logowanie po walidacji nowego hasła
            return redirect('login')
        else:
            messages.error(request, 'Błędne dane w formularzu.')
            return render(request=request, template_name='donation_app/change-password.html', context={'form': form})
