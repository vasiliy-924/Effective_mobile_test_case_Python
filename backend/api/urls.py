from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.mock_views import MockBookListView, MockOrderDetailView
from api.views import (
    CurrentUserDeleteView,
    CurrentUserView,
    LoginView,
    LogoutView,
    RegisterView,
    RuleViewSet,
)


api_v1_router = DefaultRouter()

api_v1_router.register(
    r"rules",
    RuleViewSet,
    basename="rules"
)

auth_urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
demo_urlpatterns = [
    path("books/", MockBookListView.as_view(), name="books"),
    path("order/<int:pk>/", MockOrderDetailView.as_view(), name="order"),
]
users_urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="me"),
    path("me/delete/", CurrentUserDeleteView.as_view(), name="me-delete"),
]

urlpatterns = [
    path("auth/", include((auth_urlpatterns, "auth"))),
    path("users/", include((users_urlpatterns, "users"))),
    path("demo/", include((demo_urlpatterns, "demo"))),
    path("", include(api_v1_router.urls))
]
