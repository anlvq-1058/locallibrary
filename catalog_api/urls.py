from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'book-list', views.ApiBookListView, basename='book-api')

urlpatterns = [
  path('', include(router.urls)),
  path('renew_book/<uuid:pk>', views.ApiRenewBook.as_view(), name='renew-book'),
  path('borrow_book/', views.ApiBorrowBook.as_view(), name='renew-book'),
  path('schema/', SpectacularAPIView.as_view(), name= 'schema'),
  path('schema/docs', SpectacularSwaggerView.as_view(url_name="schema")),
  path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
