from django.contrib import admin
from .models import MenuDish

class MenuDishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')  # Les champs à afficher dans l'interface d'administration

admin.site.register(MenuDish, MenuDishAdmin)


