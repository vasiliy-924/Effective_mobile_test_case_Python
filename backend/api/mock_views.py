from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        allowed = True
        if not allowed:
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
        return Response(
            {
                "resource": "book",
                "items": [{"id": 1, "title": "Мок-книга"}]
            },
            status=status.HTTP_200_OK,
        )
