from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")  # verbose_name для названия колонки в админке
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")  # blank=True - означает, что поле может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")  # Устанавливает текущую дату и уже не будет менятся
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")  # Устанавливает текущую дату и может менятся
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")   # Поле для связи с таблицой категорий(многие к одному)

    # обращение к обьекту модели вернет читаемое название
    def __str__(self):
        return self.title

    # формирование ссылки на детальный просмотр, вызывается этот метод в шаблоне, в href
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Смена названия таблицы в админке
    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'   # Для множественного
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # Смена названия таблицы в админке
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'  # Для мнжественного
        ordering = ['id']




