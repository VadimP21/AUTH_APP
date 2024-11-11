"""
Основная точка входа в проект, содержит стартовые urls
"""
from django.contrib import admin
from django.urls import path, include

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("apps.account.urls")),

]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__", include("debug_toolbar.urls"))
    )
