from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def index_view(request):
    return HttpResponse('<a href="/pages/page1">Page 1</a><br><a href="/pages/page2">Page 2</a>')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', index_view),
]