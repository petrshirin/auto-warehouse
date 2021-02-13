from django.urls import path, include
from .views import load_cargo_view, unload_cargo_view, \
    transfer_cargo_view, load_cargo_file_view

urlpatterns = [
    path('load/', load_cargo_view),
    path('unload/', unload_cargo_view),
    path('transfer/', transfer_cargo_view),
    path('load_info/', load_cargo_file_view)
]
