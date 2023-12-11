from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'book-list', views.ApiBookListView, basename='book-api')

urlpatterns = [
  path('', include(router.urls)),
  path('renew_book/<uuid:pk>', views.ApiRenewBook.as_view(), name='renew-book'),
  path('borrow_book/', views.ApiBorrowBook.as_view(), name='renew-book'),
]