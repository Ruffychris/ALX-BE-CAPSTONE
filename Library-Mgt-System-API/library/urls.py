from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, BorrowViewSet, ReturnViewSet

router = DefaultRouter()

router.register("books", BookViewSet)
router.register("members", MemberViewSet)
router.register("borrows", BorrowViewSet)
router.register("returns", ReturnViewSet)

urlpatterns = [
    path("", include(router.urls)),
]