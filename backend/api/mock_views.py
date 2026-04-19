from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.services import HTTP_METHOD_TO_ACTION, user_has_element_access


class MockOrkerDetailView(APIView):
    """
    Mock detail view for an order resource.

    Returns static data for a given order ID if the user is authenticated.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """
        GET: Return static order detail if user is authenticated.
        """
        action = HTTP_METHOD_TO_ACTION.get(request.method)
        if action is None:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not user_has_element_access(
            request.user,
            "order",
            action,
            owner_id=request.user.pk,
        ):
            return Response(
                {"detail": "Нет прав на этот ресурс."},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            {
                "resource": "order",
                "id": int(pk),
                "title": "Тестовый заказ",
            },
            status=status.HTTP_200_OK,
        )


class MockBookListView(APIView):
    """
    Mock view for a books resource.

    This view returns static data representing a list of books.
    Only authenticated users have access.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Handle GET request.

        Returns:
            Response: A Response object containing a static list of books.
        """
        action = HTTP_METHOD_TO_ACTION.get(request.method)
        if action is None:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not user_has_element_access(
            request.user,
            "book",
            action,
            owner_id=None,
        ):
            return Response(
                {"detail": "Нет прав на этот ресурс."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {
                "resource": "book",
                "items": [{"id": 1, "title": "Мок-книга"}]
            },
            status=status.HTTP_200_OK,
        )
