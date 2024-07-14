from django.urls import path, re_path

from users.routes.auth import *
from users.routes.gallery import *

app_name = 'users'

urlpatterns = [
    re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$',
            register_by_access_token),
    re_path('api/login-by-access-token/' + r'social/(?P<backend>[^/]+)/$',
            login_by_access_token),
    re_path('api/logout/' + r'social/(?P<backend>[^/]+)/$', logout_view),
    path('api/authentication-test/', authentication_test),
    path('api/get-gallery-test/', get_gallery_test),
]
