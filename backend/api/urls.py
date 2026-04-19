from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from api.views import (
#   UserViewSet
# )


api_v1_router = DefaultRouter()

api_v1_router.register(
    r"users",
    UserViewSet,
    basename="users"
)

auth_urlpatterns = [
    path("", include("djoser.urls.authtoken")),
]

urlpatterns = [
    path("auth/", include((auth_urlpatterns, "auth"))),
    path("", include(api_v1_router))
]
