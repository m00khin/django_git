from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('items', views.show_all, name='main'),
    path('items/<int:item_id>', views.show_item, name='item')
]
