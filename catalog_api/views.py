from rest_framework import viewsets, generics as gn
from rest_framework.response import Response
from catalog.models import Book, Author, BookInstance, Genre
from catalog_api.serializers import BooksSerializer, BookInstanceSerializer

class ApiBookListView(viewsets.ModelViewSet):
  queryset = Book.objects.all().order_by('title')
  serializer_class = BooksSerializer

class ApiRenewBook(gn.RetrieveUpdateDestroyAPIView):
  serializer_class = BookInstanceSerializer
  queryset = BookInstance.objects.all()
  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)

class ApiBorrowBook(gn.ListCreateAPIView):
  serializer_class = BookInstanceSerializer
  def get_queryset(self):
    queryset = BookInstance.objects.filter(borrower = self.request.user)
    return queryset
