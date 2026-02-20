from django.contrib import admin

from menuapp.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "menu", "title", "parent", "url", "named_url")
    list_filter = ("menu",)
    search_fields = ("title", "url", "named_url")

