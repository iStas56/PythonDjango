from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# Класс для отображения главной страницы
class WomenHome(DataMixin, ListView):
    model = Women   # Выберает все записи из таблицы и пытается вывести в виде списка
    template_name = 'women/index.html'
    context_object_name = 'posts'   # Чтобы в шаблоне в posts передать объект('posts': posts)
    # extra_context = {'title': 'Главная страница'} # Так можно передатьт только статический контекст, динамически, а сним и статический передается в get_context_data

    # Передать динамические данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) # Получаем то, что уже передано в контекст, чтобы не затереть
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items())) # Объеденяем то что пришло с миксина и текущие данные
        return context

    # Фильтрация выборки
    def get_queryset(self):
        return Women.objects.filter(is_published=True)

# Метод представления для главной страницы с помощью функций
# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'title': 'Главная страница',
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    context = {'title': 'О сайте', 'menu': menu}
    return render(request, 'women/about.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # Редирект при успешном добавлении, если в модели не прописан get_absolute_url
    login_url = reverse_lazy('home')    # Если неавторизован, то перенаправится на главную
    raise_exception = True  # Если неавторизован, то  ошибка 404

    # Передать динамические данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем то, что уже передано в контекст, чтобы не затереть
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))  # Объеденяем то что пришло с миксина и текущие данные


# def addpage(request):
#
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES) # Для загрузки изображений request.FILES
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()    # Экземпляр формы
#
#     context = {
#         'title': 'Добавление статьи',
#         'form': form,
#     }
#     return render(request, 'women/addpage.html', context)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug) # Если нет такого слага то вернет 404
#
#     context = {
#         #'title': 'Отображение по рубрикам',
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


# Класс представление для отображения категорий
class WomanCategory(DataMixin, ListView):
    model = Women  # Выберает все записи из таблицы и пытается вывести в виде списка
    template_name = 'women/index.html'
    context_object_name = 'posts'  # Чтобы в шаблоне в posts передать объект('posts': posts)
    allow_empty = False # Если нет поста по указанному слагу то генерим 404

    # Передать динамические данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем то, что уже передано в контекст, чтобы не затереть
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    # Фильтрация выборки
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)    # Я хз как но по фильтру cat__slug как то вытаскивает нужные рубрики
#
#     # Если передастся айди с несущ категорией, то из БД ничего не выберется, генерим 404
#     if len(posts) == 0:
#         raise Http404
#
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)


# Вторым параметром(catid) передаем айди категории для показа(ну так же можно передавать и для удаления записи)
def categories(request, catid):
    # проверим содержатся ли в строке параметры
    if request.GET:
        print(request.GET)  # на запрос http://127.0.0.1:8000/cats/1985/?name=Stas&surname=Ardashev выведет в консоль словарь ключ - значение
        print(request.GET['name'])  # Выведет значение

    return HttpResponse(f'It is a {catid} category!')   # Для форматирования строки, вставка параметра



def archive(request, year):
    if int(year) > 2021:
        # raise Http404  - можно выдать 404 если год выше чем сейчас или ниже редиректить
        return redirect('home', permanent=True)    # Если год выше, чем текущий, то редиректим на главную, если permanent=True то постоянный редирект(301)

    return HttpResponse(f"Архив за {year} год")


# Функция обработчик несуществующих страниц
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')