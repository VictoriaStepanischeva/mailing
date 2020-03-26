from django.conf.urls import url
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken


from mailing.apps.users.api.views import RegisterUserView, LogoutUserView

urlpatterns = [
    url(r'^register/', RegisterUserView.as_view(), name='user_register'),
    url(r'^login/', ObtainJSONWebToken.as_view(),
         name='token_obtain_pair'),
    url(r'^logout/', LogoutUserView.as_view(),
        name='token_logout'),
    url(r'^token/refresh/', RefreshJSONWebToken.as_view(),
         name='token_refresh'),
    ]