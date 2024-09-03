from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


"""В Django REST Framework, Router используется для автоматического создания
URL-маршрутов для ваших ViewSet. Это удобный инструмент, который упрощает
настройку маршрутизации и обеспечивает автоматическое сопоставление
стандартных CRUD операций с соответствующими HTTP методами и URL

Виды ViewSets
1. DefaultRouter: Предоставляет стандартный набор маршрутов и добавляет
маршрут для страницы API корня.
2. SimpleRouter: Похож на DefaultRouter, но не добавляет маршрут для страницы
API корня."""
router = DefaultRouter()
router.register(r'housing', HousingViewSet)
router.register(r'adverts', AdvertsViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="First API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    # BasicAuthentication / TokenAuthentication
    path('protected/', ProtectedDataView.as_view(), name='protected-data'),
    path('api-tocken-auth/', obtain_auth_token, name='api-tocken-auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # # Simple JWT:
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin'),

    # Включение маршрутов, созданных роутером
    path('', include(router.urls)),

    # re_path(r'^housing/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', books_by_date_view, name='housing'),
    # path('user-book/', UserBookListView.as_view(), name='user-book'),
    # # path('books/', BookListCreateView.as_view(), name='book-list-create'),
    # path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'),
    # # path('books/expensive/', ExpensiveBooksView.as_view(), name='book-expensive'),
    # path('books/', BookListView.as_view(), name='book-list-create'),  # Для получения всех книг и создания новой книги
    # path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'), # Для операций с одной книгой
   ]