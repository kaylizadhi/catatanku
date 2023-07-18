from django.urls import path
from notes.views import *

urlpatterns = [
    path('', index, name='index'),
    path('create', create, name='create'),
    path('created', create_note),
    path('<id>', read),
    path('<id>/update', update),
    path('<id>/delete', delete),
    path('<id>/json', show_json_by_id, name="show_json_by_id"),
]