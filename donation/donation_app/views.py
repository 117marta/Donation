from django.shortcuts import render
from django.views import View
from .models import Category, Institution, Donation


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