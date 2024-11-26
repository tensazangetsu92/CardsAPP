# myapp/urls.py
from django.urls import path
from .views import show_collections, add_collection, delete_collection, show_cards, add_card, delete_cards, \
    rename_collection

urlpatterns = [
    path('show_collections/', show_collections, name='show_collections'),
    path('add_collection/',add_collection ,name='add_collection'),
    path('rename_collection/<int:collection_id>/', rename_collection ,name='rename_collection'),
    path('delete_collection/<int:collection_id>/', delete_collection, name='delete_collection'),
    path('show_cards/<int:collection_id>/', show_cards, name='show_cards'),
    path('add_card/<int:collection_id>/', add_card ,name='add_card'),
    path('delete_cards/<int:collection_id>/', delete_cards ,name='delete_cards'),
]