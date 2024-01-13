from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers import CommentSerializer


class CommentPagination(PageNumberPagination):
    page_size = 25


class CommentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.filter(parent_comment__isnull=True).order_by('-date_added')
    serializer_class = CommentSerializer
    pagination_class = CommentPagination


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
