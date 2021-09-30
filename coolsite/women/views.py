from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

# Метод представления для главной страницы
def index(request):
    posts = Women.objects.all()

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    context = {'title': 'О сайте'}
    return render(request, 'women/about.html', context=context)


def addpage(request):

    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES) # Для загрузки изображений request.FILES
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()    # Экземпляр формы

    context = {
        'title': 'Добавление статьи',
        'form': form,
    }
    return render(request, 'women/addpage.html', context)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug) # Если нет такого слага то вернет 404

    context = {
        'title': 'Отображение по рубрикам',
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    posts = Women.objects.filter(cat__slug=cat_slug)    # Я хз как но по фильтру cat__slug как то вытаскивает нужные рубрики

    # Если передастся айди с несущ категорией, то из БД ничего не выберется, генерим 404
    if len(posts) == 0:
        raise Http404

    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug,
    }

    return render(request, 'women/index.html', context=context)


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