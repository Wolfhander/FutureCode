from django.urls import path
from . import views

urlpatterns = [
    path('page1/', views.page1_view, name='page1'),
    path('page2/', views.page2_view, name='page2'),
]