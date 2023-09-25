from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from recipes.paginations import CustomPagination
from recipes.permissions import AuthorOrReadOnlyPermission
from users.models import User, UserFollow
from .serializers import CustomUserSerializer, UserFollowSerializer


class CustomUserViewSet(UserViewSet):
    """ViewSet для пользователей."""

    queryset = User.objects.all()
    permission_classes = (AuthorOrReadOnlyPermission,)
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        """
        Получает и возвращает список подписок для
        аутентифицированного пользователя.
        """
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        subs = User.objects.filter(following__user=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(subs, request)
        serializer = UserFollowSerializer(
            page, many=True, context={"request": request}
        )
        response_data = {
            "count": subs.count(),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data,
        }
        return Response(response_data)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, id):
        """Подписывает пользователя на автора"""
        following = get_object_or_404(User, pk=id)

        serializer = UserFollowSerializer(
            data=request.data,
            context={"request": request, "instance": following},
        )
        serializer.is_valid(raise_exception=True)

        if request.method == "POST":
            follow = UserFollow.objects.create(
                user=request.user, following=following
            )
            serializer = UserFollowSerializer(
                following, context={"request": request}
            )
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )

        follow = get_object_or_404(
            UserFollow, user=request.user, following=following
        )
        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
