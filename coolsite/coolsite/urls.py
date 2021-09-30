from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coolsite import settings
from women.views import pageNotFound    ## Импортирую функцию обработчик

urlpatterns = [
    path('admin/', admin.site.urls),  # маршрут для админки
    path('', include('women.urls')),  # подключаю маршрут из приложения
]

# для загрузки файлов в отладочном режиме добавится маршрут
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчик для несуществующих страниц
handler404 = pageNotFound