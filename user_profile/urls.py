from django.urls import path, include
from .views import register_user_view, self_info_view, \
    check_registration_code_view, get_user_view, search_users_view

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration', register_user_view),
    path('check_registration_code', check_registration_code_view),
    path('my/', self_info_view),
    path('search/', search_users_view),
    path('get/<int:pk>', get_user_view)
]