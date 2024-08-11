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
    re_path('api/authentication-test/' + r'social/(?P<backend>[^/]+)/$',
            authentication_test),
    re_path('api/get-gallery-test/' + r'social/(?P<backend>[^/]+)/$',
            get_gallery_test),
    path('api/email-registration/', email_registration_view),
    path('api/activate/', activate, name='activate'),
    re_path('api/upload-gallery-test/' + r'social/(?P<backend>[^/]+)/$',
            upload_gallery_test)
]
