from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tel_book.views.contact_views import *
from tel_book.views.auth_views import *
from tel_book.views.import_views import import_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('phone_book/', show_phone_book),
    path('login/', login, name='register'),
    path('reg/', register, name='register'),
    path('logout/', logout),
    path('add/', add_contact, name='add_contact'),
    path('delete_contact/<int:id>/', delete_contact, name='delete_contact'),
    path('contact/<int:id>/edit/', edit_contact, name='edit_contact'),
    path('import-csv/', import_csv, name='import_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
