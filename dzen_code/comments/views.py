# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
#
# from .models import Comment
# from .serializers import CommentSerializer
#
#
# class CommentPagination(PageNumberPagination):
#     page_size = 25
#
#
# class CommentListCreateView(ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Comment.objects.filter(parent_comment__isnull=True).order_by('-date_added')
#     serializer_class = CommentSerializer
#     pagination_class = CommentPagination
#
#
# class CommentDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
from datetime import timezone

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


from .models import Comment
from .serializers import CommentSerializer


class CommentPagination(PageNumberPagination):
    page_size = 25


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['parent_comment']
    ordering_fields = ['user__username', 'user__email', 'date_added']
    ordering = ['-date_added']
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, date_added=timezone.now())


"""
це клас, який буде використовуватись після під'єднання фронтенду
щоб при натисканні на його елементи вилазили його нащадки
"""
# class CommentListCreateView(generics.ListCreateAPIView):
#     serializer_class = CommentSerializer
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['parent_comment']
#     ordering_fields = ['user__username', 'user__email', 'date_added']
#     ordering = ['-date_added']
#     pagination_class = CommentPagination
#
#     def get_queryset(self):
#         return Comment.objects.filter(parent_comment__isnull=True).order_by('-date_added')
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user, date_added=timezone.now())


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer