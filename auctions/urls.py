from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories_view", views.categories_view, name="categories_view"),
    path("<int:id>", views.listing_view, name="listing_view")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
