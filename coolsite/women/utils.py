from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'},]


class DataMixin:
    paginate_by = 3  # Количество элементов на странице(для классов представления)

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women')) # Подсчитает посты у каждой рубрики и создаст словарь women__count(используется в шаблоне)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        # context['menu'] = menu  # Добавляем данные в контекст. Т.к. у меня меню реализовано с помощью тегов, этот вариант не используется
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context