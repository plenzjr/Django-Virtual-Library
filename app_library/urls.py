from rest_framework import routers
from app_library.apis import views
from django.urls import path, include


router = routers.DefaultRouter()

router.register(r'authors', views.AuthorViewSet)
router.register(r'book_review', views.BookReviewViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'publisher', views.PublisherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
