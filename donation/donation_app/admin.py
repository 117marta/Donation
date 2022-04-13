from django.contrib import admin, messages
from .models import Category, Institution, Donation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.unregister(User)

@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff')
    readonly_fields = ['date_joined',]  # This information should never be changed by any user - not editable
    actions = ['delete_selected']

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

    def delete_selected(self, request, queryset):  # DOPRACOWAĆ!!!
        cnt = User.objects.filter(is_superuser=True)

        for obj in queryset:
            if cnt.count() == 1:
                self.message_user(request, 'Nie możesz usunąć ostatniego admina!')
            else:
                messages.success = f'Tyle jest adminów: {queryset.count()}'
                self.message_user(request, f'Usunięto użytkownika: {obj.username}. Pozostało adminów: {queryset.count()}')
                obj.delete()
    delete_selected.short_description = 'Usuń wybranych użytkowników'


admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)

