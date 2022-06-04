from django.contrib import admin, messages
from .models import Category, Institution, Donation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.unregister(User)

@admin.register(User)
class MyUserAdmin(UserAdmin):
# class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_superuser', 'is_staff')  # wyświetlanie
    ordering = ('-is_superuser', 'username')  # kolejność wyświetlania
    list_filter = ('is_superuser', 'is_active', 'is_staff')  # filtrowanie
    readonly_fields = ['date_joined',]  # This information should never be changed by any user - not editable
    actions = ['delete_selected', 'make_admin', 'degrade_user', 'activate_user', 'deactivate_user']
    # fieldsets = (
    #     (None, {'fields': ('username', 'date_joined')}),
    #     ('Dane', {'fields': ('first_name', 'last_name', 'email', 'password')}),
    #     ('Pozwolenia', {'fields': ('is_superuser', 'is_staff')}),
    # )  # edycja pól na karcie użytkownika

    def get_form(self, request, obj=None, **kwargs):  # obj is the instance you currently operate on
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:  # prevent non-superusers from changing a user’s username
            form.base_fields['username'].disabled = True

        return form

    # def has_delete_permission(self, request, obj=None):
    #     admins_all = User.objects.filter(is_superuser=True)
    #     print(admins_all)
    #     if admins_all.count() > 1:
    #         return True
    #     else:
    #         self.message_user(request, 'Został ostatni admin!')
    #         return False  # nie będzie przycisku 'Usuń' na karcie użytkownika

    def delete_selected(self, request, queryset):
        admins = User.objects.filter(is_superuser=True)

        for obj in queryset:  # tyle queryset ile zaznaczonych userów (obj)
            if obj in User.objects.filter(username=request.user):
                self.message_user(request, 'Nie można usunąć samego siebie!')
            elif admins.count() == 1:
                self.message_user(request, 'Nie możesz usunąć ostatniego admina!')
            else:
                obj.delete()
                self.message_user(request, f'Usunięto użytkownika: {obj.username}. Pozostało adminów: {admins.count()}')
    delete_selected.short_description = 'Usuń zaznaczonych użytkowników!'

    def make_admin(self, request, queryset):
        queryset.update(is_superuser=True)
        self.message_user(request, 'Adminem został/a/li: {}.'.format(", ".join([u.username for u in queryset])))
    make_admin.short_description = 'Awansuj na admina!'

    def degrade_user(self, request, queryset):
        queryset.update(is_superuser=False)
        self.message_user(request, f'Zdegradowano: {", ".join([u.username for u in queryset])}.')
    degrade_user.short_description = 'Zdegraduj użytkownika/ów!'

    def activate_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Aktywowano użytownika/ów: {", ".join([u.username for u in queryset])}.')
    activate_user.short_description = 'Aktywuj użytkownika/ów!'

    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Dezaktywowano użytkownia/ów: {", ".join([u.username for u in queryset])}.')
    deactivate_user.short_description = 'Dezaktywuj użytkownika/ów!'


admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)

