from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, filters, permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    # Prevent multiple likes
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_Request
)


    # Create notification (don’t notify yourself)
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        )

    return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if not like:
        return Response(
            {"detail": "You have not liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    like.delete()

    return Response(
        {"detail": "Post unliked successfully."},
        status=status.HTTP_200_OK
    )

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # filtering/search
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "title"]
    filterset_fields = ["author"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # posts from users I follow
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
