from django.urls import path
from notes.views import *

urlpatterns = [
    path('', index, name='index'),
    path('create', create, name='create'),
    path('created', create_note),
    path('json', show_json),
    path('post', post_note),
    path('delete-post', delete_flutter),
    path('put', update_flutter),
    path('<id>', read),
    path('<id>/update', update),
    path('<id>/delete', delete),
    path('<id>/json', show_json_by_id, name="show_json_by_id"),
]