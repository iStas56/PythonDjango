from django.contrib import admin

from .models import *

# Вспомогательный класс, чтобы в админке отобразить больше полей
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # Список полей для отображения
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}  # Будет автоматически создавать URL транслитом от названия поля

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Список полей для отображения
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}   # Будет автоматически создавать URL транслитом от названия поля

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
