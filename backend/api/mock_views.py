from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import HasElementAccess


class MockOrderDetailView(APIView):
    """
    Mock detail view for an order resource.

    Returns static data for a given order ID if the user is authenticated.
    """

    permission_classes = (IsAuthenticated, HasElementAccess)
    element_code = "order"

    def get_owner_id(self, request):
        return request.user.pk

    def get(self, request, pk):
        """
        GET: Return static order detail if user is authenticated.
        """
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
    permission_classes = (IsAuthenticated, HasElementAccess)
    element_code = "book"

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
