from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet
from api.mock_views import MockBookListView, MockOrkerDetailView


api_v1_router = DefaultRouter()

api_v1_router.register(
    r"users",
    UserViewSet,
    basename="users"
)

auth_urlpatterns = [
    path("", include("djoser.urls.authtoken")),
]
demo_urlpattens = [
    path("books/", MockBookListView.as_view(), name="books"),
    path("order/", MockOrkerDetailView.as_view(), name="order")
]

urlpatterns = [
    path("auth/", include((auth_urlpatterns, "auth"))),
    path("demo/", include((demo_urlpattens, "demo"))),
    path("", include(api_v1_router.urls))
]
